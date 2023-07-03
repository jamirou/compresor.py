import os
import zipfile
import shutil
import zlib
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
        return {'message': 'file successfully uploaded.'}
    else:
        return jsonify({'message': 'Error uploading file. Make sure it is a file with the valid format.'}), 400


@app.route('/compress', methods=['POST'])
def compress():
    global compressed_file  # Acceder a la variable global

    # Obtener el archivo del formulario
    file = request.files['file']
    # Verificar si se seleccionó un archivo
    if file.filename == '':
        return jsonify({'message': 'No files selected.'}), 400
    # Obtener el nombre del archivo original sin la extensión
    filename = os.path.splitext(file.filename)[0]
    # Ruta del archivo comprimido con el nombre del archivo original
    zip_filename = os.path.join('uploads', f'{filename}.zip')
    # Ruta del archivo original
    original_filename = os.path.join('uploads', secure_filename(file.filename))
    # Guardar el archivo original en la carpeta "uploads"
    file.save(original_filename)

    # Crear el archivo ZIP con mayor compresión
    with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write(original_filename, os.path.basename(original_filename))

    # Asignar el archivo comprimido a la variable global
    compressed_file = zip_filename

    return {'message': 'Successful compression.', 'download_url': '/download'}

@app.route('/download')
def download():
    global compressed_file  # Acceder a la variable global

  # Verificar si hay un archivo comprimido almacenado en la variable global
    if compressed_file is None:
        return jsonify({'message': 'No compressed file available.'}), 404

    # Enviar el archivo comprimido como descarga
    return send_file(compressed_file, as_attachment=True)
    
@app.route('/delete', methods=['POST'])
def delete():
    global compressed_file  # Acceder a la variable global
    global uploaded_file 

    # Verificar si hay un archivo comprimido almacenado en la variable global
    if compressed_file is None:
        return jsonify({'message': 'No compressed file available.'}), 404

    # Eliminar el archivo comprimido
    os.remove(compressed_file)
    compressed_file = None

    # Verificar si hay un archivo subido almacenado en la variable global
    if uploaded_file is None:
        return jsonify({'message': 'No compressed file available.'}), 404

    # Obtener la ruta del archivo subido
    filename = os.path.join('uploads', secure_filename(uploaded_file.filename))

    # Verificar si el archivo subido existe
    if os.path.exists(filename):
        # Eliminar el archivo subido
        os.remove(filename)
        uploaded_file = None

        return {'message': 'Successfully deleted files.'}
    else:
        return jsonify({'message': 'The uploaded file does not exist.'}), 404


if __name__ == '__main__':
    app.run()