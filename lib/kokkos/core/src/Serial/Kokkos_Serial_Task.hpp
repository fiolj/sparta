//@HEADER
// ************************************************************************
//
//                        Kokkos v. 4.0
//       Copyright (2022) National Technology & Engineering
//               Solutions of Sandia, LLC (NTESS).
//
// Under the terms of Contract DE-NA0003525 with NTESS,
// the U.S. Government retains certain rights in this software.
//
// Part of Kokkos, under the Apache License v2.0 with LLVM Exceptions.
// See https://kokkos.org/LICENSE for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//@HEADER

#ifndef KOKKOS_IMPL_SERIAL_TASK_HPP
#define KOKKOS_IMPL_SERIAL_TASK_HPP

#include <Kokkos_Macros.hpp>
#if defined(KOKKOS_ENABLE_TASKDAG)

#include <Kokkos_TaskScheduler_fwd.hpp>

#include <Serial/Kokkos_Serial.hpp>
#include <impl/Kokkos_HostThreadTeam.hpp>
#include <impl/Kokkos_TaskQueue.hpp>
#include <impl/Kokkos_TaskTeamMember.hpp>

//----------------------------------------------------------------------------
//----------------------------------------------------------------------------

#ifdef KOKKOS_ENABLE_DEPRECATION_WARNINGS
// We allow using deprecated classes in this file
KOKKOS_IMPL_DISABLE_DEPRECATED_WARNINGS_PUSH()
#endif

namespace Kokkos {
namespace Impl {

template <class QueueType>
class TaskQueueSpecialization<SimpleTaskScheduler<Kokkos::Serial, QueueType>> {
 public:
  // Note: Scheduler may be an incomplete type at class scope (but not inside
  // of the methods, obviously)

  using execution_space = Kokkos::Serial;
  using memory_space    = Kokkos::HostSpace;
  using scheduler_type  = SimpleTaskScheduler<Kokkos::Serial, QueueType>;
  using member_type =
      TaskTeamMemberAdapter<HostThreadTeamMember<Kokkos::Serial>,
                            scheduler_type>;

  static void execute(scheduler_type const& scheduler) {
    using task_base_type = typename scheduler_type::task_base_type;

    auto const& serial_execution_space = scheduler.get_execution_space();

    // Set default buffers
    serial_execution_space.impl_internal_space_instance()
        ->resize_thread_team_data(0,   /* global reduce buffer */
                                  512, /* team reduce buffer */
                                  0,   /* team shared buffer */
                                  0    /* thread local buffer */
        );

    auto& self = serial_execution_space.impl_internal_space_instance()
                     ->m_thread_team_data;

    auto& queue         = scheduler.queue();
    auto team_scheduler = scheduler.get_team_scheduler(0);

    member_type member(scheduler, self);

    auto current_task = OptionalRef<task_base_type>(nullptr);

    while (!queue.is_done()) {
      // Each team lead attempts to acquire either a thread team task
      // or a single thread task for the team.

      // pop a task off
      current_task = queue.pop_ready_task(team_scheduler.team_scheduler_info());

      // run the task
      if (current_task) {
        current_task->as_runnable_task().run(member);
        // Respawns are handled in the complete function
        queue.complete((*std::move(current_task)).as_runnable_task(),
                       team_scheduler.team_scheduler_info());
      }
    }
  }

  static constexpr uint32_t get_max_team_count(
      execution_space const&) noexcept {
    return 1;
  }

  template <typename TaskType>
  static void get_function_pointer(typename TaskType::function_type& ptr,
                                   typename TaskType::destroy_type& dtor) {
    ptr  = TaskType::apply;
    dtor = TaskType::destroy;
  }
};

//----------------------------------------------------------------------------

template <class Scheduler>
class TaskQueueSpecializationConstrained<
    Scheduler, std::enable_if_t<std::is_same_v<
                   typename Scheduler::execution_space, Kokkos::Serial>>> {
 public:
  // Note: Scheduler may be an incomplete type at class scope (but not inside
  // of the methods, obviously)

  using execution_space = Kokkos::Serial;
  using memory_space    = Kokkos::HostSpace;
  using scheduler_type  = Scheduler;
  using member_type =
      TaskTeamMemberAdapter<HostThreadTeamMember<Kokkos::Serial>,
                            scheduler_type>;

  static void iff_single_thread_recursive_execute(
      scheduler_type const& scheduler) {
    using task_base_type = TaskBase;
    using queue_type     = typename scheduler_type::queue_type;

    auto* const end = reinterpret_cast<task_base_type*>(task_base_type::EndTag);

    execution_space serial_execution_space;
    auto& data = serial_execution_space.impl_internal_space_instance()
                     ->m_thread_team_data;

    member_type exec(scheduler, data);

    // Loop until no runnable task

    task_base_type* task = end;

    auto* const queue = scheduler.m_queue;

    do {
      task = end;

      for (int i = 0; i < queue_type::NumQueue && end == task; ++i) {
        for (int j = 0; j < 2 && end == task; ++j) {
          task = queue_type::pop_ready_task(&queue->m_ready[i][j]);
        }
      }

      if (end == task) break;

      (*task->m_apply)(task, &exec);

      queue->complete(task);

    } while (1);
  }

  static void execute(scheduler_type const& scheduler) {
    using task_base_type = TaskBase;
    using queue_type     = typename scheduler_type::queue_type;

    auto* const end = reinterpret_cast<task_base_type*>(task_base_type::EndTag);

    execution_space serial_execution_space;

    // Set default buffers
    serial_execution_space.impl_internal_space_instance()
        ->resize_thread_team_data(0,   /* global reduce buffer */
                                  512, /* team reduce buffer */
                                  0,   /* team shared buffer */
                                  0    /* thread local buffer */
        );

    auto* const queue = scheduler.m_queue;

    auto& data = serial_execution_space.impl_internal_space_instance()
                     ->m_thread_team_data;

    member_type exec(scheduler, data);

    // Loop until all queues are empty
    while (0 < queue->m_ready_count) {
      task_base_type* task = end;

      for (int i = 0; i < queue_type::NumQueue && end == task; ++i) {
        for (int j = 0; j < 2 && end == task; ++j) {
          task = queue_type::pop_ready_task(&queue->m_ready[i][j]);
        }
      }

      if (end != task) {
        // pop_ready_task resulted in lock == task->m_next
        // In the executing state

        (*task->m_apply)(task, &exec);

        // If a respawn then re-enqueue otherwise the task is complete
        // and all tasks waiting on this task are updated.
        queue->complete(task);
      } else if (0 != queue->m_ready_count) {
        Kokkos::abort("TaskQueue<Serial>::execute ERROR: ready_count");
      }
    }
  }

  template <typename TaskType>
  static void get_function_pointer(typename TaskType::function_type& ptr,
                                   typename TaskType::destroy_type& dtor) {
    ptr  = TaskType::apply;
    dtor = TaskType::destroy;
  }
};

extern template class TaskQueue<Kokkos::Serial,
                                typename Kokkos::Serial::memory_space>;

}  // namespace Impl
}  // namespace Kokkos

#ifdef KOKKOS_ENABLE_DEPRECATION_WARNINGS
KOKKOS_IMPL_DISABLE_DEPRECATED_WARNINGS_POP()
#endif

//----------------------------------------------------------------------------
//----------------------------------------------------------------------------

#endif /* #if defined( KOKKOS_ENABLE_TASKDAG ) */
#endif /* #ifndef KOKKOS_IMPL_SERIAL_TASK_HPP */
