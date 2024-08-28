from pathlib import Path

p = Path("doc/web/")

maxlines = 20


def add_index(s):
  "Add one line with to include the command in the index"
  if has_index(s):
    return s

  Ls = s.split('\n')
  indices = []
  for j, line in enumerate(Ls[:maxlines]):  # only first lines
    if "######" in line:
      # Tenemos el elemento donde empieza el título
      indices.append(Ls[j + 1].replace(" command", ""))

  tt = ["\n.. index:: {}".format(i) for i in indices if i.strip() != ""]
  Ls.insert(1, "".join(tt))
  return "\n".join(Ls)


def has_index(s):
  return ".. index::" in s[:100]


def is_command_page(s):
  return (":orphan:" in s[:100]) and (".. _command-" in s[:100])


for fn in p.glob('*.rst'):
  with fn.open() as fi:
    s = fi.read()

  if is_command_page(s):

    s1 = add_index(s)
    with fn.open("w") as fo:
      fo.write(s1)


for fn in p.glob('*.rst'):
  with fn.open() as fi:
    s = fi.read()

  if is_command_page(s):
    print(fn.name)
