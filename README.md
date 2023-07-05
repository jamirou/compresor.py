# Compresor de Archivos

Este proyecto es un compresor de archivos desarrollado principalmente con Python, JS, HTML y CSS. Utiliza las siguientes bibliotecas de Python: `flask`, `os`, `zipfile`, `shutil` y `zlib`.

## Funcionalidades

El compresor de archivos ofrece las siguientes funcionalidades:

- Cargar un archivo: Permite al usuario seleccionar y cargar un archivo desde su dispositivo.
- Comprimir archivo: Comprime el archivo cargado utilizando el algoritmo de compresión ZIP con la máxima compresión.
- Descargar archivo comprimido: Proporciona un enlace para descargar el archivo comprimido.
- Eliminar archivo comprimido: Permite al usuario eliminar el archivo comprimido y el archivo original cargado.

## Requisitos

El proyecto requiere tener instalado Python y las siguientes bibliotecas de Python:

- Flask
- Werkzeug

## Configuración

1. Clona el repositorio o descarga los archivos del proyecto.
2. Instala las bibliotecas de Python requeridas usando el siguiente comando:
-pip install -r requirements.txt


## Ejecución

1. Navega hasta el directorio raíz del proyecto.
2. Ejecuta el siguiente comando:


3. Abre un navegador web y accede a la siguiente URL: `http://localhost:5000`.

## Estructura del proyecto

El proyecto tiene la siguiente estructura de archivos:

- `app.py`: El archivo principal que contiene la lógica del servidor Flask.
- `app.js`: El archivo JavaScript que maneja las interacciones del cliente.
- `index.html`: El archivo HTML que define la interfaz de usuario.
- `styles.css`: El archivo CSS que define los estilos visuales.
- `uploads/`: Directorio donde se guardan los archivos cargados por los usuarios.

## Contribución

Si deseas contribuir a este proyecto, puedes seguir los siguientes pasos:

1. Realiza un fork del repositorio.
2. Crea una rama para tu contribución:
-git checkout -b feature/nueva-funcionalidad


3. Realiza tus cambios y commitea los archivos modificados:
-git commit -am 'Agrega nueva funcionalidad'


4. Sube tus cambios a tu repositorio remoto:
-git push origin feature/nueva-funcionalidad


5. Crea una pull request en el repositorio original para revisar tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Puedes consultar el archivo [LICENSE](LICENSE) para más detalles.

