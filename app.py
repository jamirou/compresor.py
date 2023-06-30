import os
import zipfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Variable global para almacenar el archivo comprimido
compressed_file = None
uploaded_file = None  # Variable global para guardar el archivo subido

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_file  # Acceder a la variable global

    # Función para verificar la extensión del archivo permitida
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    file = request.files['file']
    # Validación del archivo 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))  # Guardar el archivo en la carpeta "uploads"
        uploaded_file = file  # Asignar el archivo a la variable global
        return {'message': 'Archivo subido exitosamente.'}
    else:
        return jsonify({'message': 'Error al subir el archivo. Asegúrate de que sea un archivo con el fomato válido.'}), 400


@app.route('/compress', methods=['POST'])
def compress():
    global compressed_file  # Acceder a la variable global

    # Obtener el archivo del formulario
    file = request.files['file']

    # Verificar si se seleccionó un archivo
    if file.filename == '':
        return jsonify({'message': 'No se ha seleccionado ningún archivo.'}), 400

    # Obtener el nombre del archivo original sin la extensión
    filename = os.path.splitext(file.filename)[0]

    # Ruta del archivo comprimido con el nombre del archivo original
    zip_filename = os.path.join('uploads', f'{filename}.zip')

    # Crear el archivo comprimido
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.writestr(file.filename, file.read())

    # Asignar el archivo comprimido a la variable global
    compressed_file = zip_filename

    return {'download_url': '/download'}


@app.route('/download')
def download():
    global compressed_file  # Acceder a la variable global

  # Verificar si hay un archivo comprimido almacenado en la variable global
    if compressed_file is None:
        return jsonify({'message': 'No hay archivo comprimido disponible.'}), 404

    # Enviar el archivo comprimido como descarga
    return send_file(compressed_file, as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete():
    global compressed_file  # Acceder a la variable global
    global uploaded_file 

    # Verificar si hay un archivo comprimido almacenado en la variable global
    if compressed_file is None:
        return jsonify({'message': 'No hay archivo comprimido disponible.'}), 404

    # Eliminar el archivo comprimido
    os.remove(compressed_file)
    compressed_file = None

    # Verificar si hay un archivo subido almacenado en la variable global
    if uploaded_file is None:
        return jsonify({'message': 'No hay archivo subido disponible.'}), 404

    # Obtener la ruta del archivo subido
    filename = os.path.join('uploads', secure_filename(uploaded_file.filename))

    # Verificar si el archivo subido existe
    if os.path.exists(filename):
        # Eliminar el archivo subido
        os.remove(filename)
        uploaded_file = None

        return {'message': 'Archivos eliminados exitosamente.'}
    else:
        return jsonify({'message': 'El archivo subido no existe.'}), 404


if __name__ == '__main__':
    app.run()