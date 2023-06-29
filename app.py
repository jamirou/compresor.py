import os
import zipfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Función para verificar la extensión del archivo permitida
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    file = request.files['file']
    # Validación del archivo 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))  # Guardar el archivo en la carpeta "uploads"
        return {'message': 'Archivo subido exitosamente.'}
    else:
        return jsonify({'message': 'Error al subir el archivo. Asegúrate de que sea un archivo con el fomato válido.'}), 400


@app.route('/compress', methods=['POST'])
def compress():
    # Obtener el archivo del formulario
    file = request.files['file']

    # Verificar si se seleccionó un archivo
    if file.filename == '':
        return jsonify({'message': 'No se ha seleccionado ningún archivo.'}), 400

    # Ruta del archivo comprimido
    zip_filename = os.path.join('uploads', 'compressed.zip')

    # Crear el archivo comprimido
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.writestr(file.filename, file.read())

    return {'download_url': '/download'}

@app.route('/download')
def download():
    # Obtener la ruta del archivo comprimido
    zip_filename = os.path.join('uploads', 'compressed.zip')

    # Verificar si el archivo comprimido existe
    if os.path.exists(zip_filename):
        return send_file(zip_filename, as_attachment=True)
    else:
        return jsonify({'message': 'El archivo comprimido no existe.'}), 404


@app.route('/delete', methods=['POST'])
def delete():
    # Obtener la ruta del archivo comprimido
    zip_filename = os.path.join('uploads', 'compressed.zip')

    # Verificar si el archivo comprimido existe
    if os.path.exists(zip_filename):
        # Eliminar el archivo comprimido
        os.remove(zip_filename)

        return {'message': 'Archivo comprimido eliminado.'}
    else:
        return jsonify({'message': 'El archivo comprimido no existe.'}), 404


if __name__ == '__main__':
    app.run()