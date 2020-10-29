Tanto fetcher.py como parser.py correran indefinidamente mientras la primera linea de sus correspondientes archivos fetcher.conf y parser.conf sea distinta de 'stop'.

Para hacer una ejecucion de prueba:
    - Borrar el contenido de las carpetas fetcher-queue, parser-queue, fetcher-explored y output.
    - Copiar 01.txt a la carpeta fetcher-queue.
    - Asegurarse de que los ficheros .conf contengan como primera linea la palabra 'stop'.
    - Ejecutar fetcher.py y comprobar como se llena la carpeta parser-queue.
    - Ejecutar parser.py y comprobar como se llenan las carpetas fetcher-queue y output.
    - Continuar ejecutando sucesivamente fetcher.py y parser.py, comprobando como se llena la carpeta output.

Cuidado al ejecutar el fetcher y el parser a la vez, no he comprobado que condiciones de carrera puede haber si tratan de acceder al mismo archivo. Son necesarias 3 ejecuciones para extraer todas las tablas de la web.