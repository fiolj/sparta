# Documentación

Para crear la documentación seguimos los siguientes pasos:

1. Actualizamos el branch master desde upstream.
   Podemos hacerlo directamente desde la página de github (con el botón: Sync fork)
   y luego actualizamos la versión local
2. Checkout branch docs
3. Actualizamos el branch docs (Hacemos el merge desde master. En emacs Ctrl-x g -> m m -> elegimos master)
4. Desde el directorio docs/ hacer: `make sources`
   El Makefile ejecuta el script txt2rst.py (del proyecto de gitlab incipientes/txt2sjprst)
   Hacer un symlink desde su versión local a ~/.local/bin para que lo encuentre.
5. Agregamos todos los archivos en doc/ (git add) y hacemos el commit
6. Hacemos el push del branch docs

