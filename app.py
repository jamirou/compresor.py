import os
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
    # Aquí debes implementar la lógica para comprimir el archivo.
    # Utiliza el módulo 'zipfile' de Python para crear el archivo comprimido.
    # Puedes agregar mensajes de registro en la consola para seguir el progreso.
    return {'download_url': '/download'}

@app.route('/download')
def download():
    # Aquí debes devolver el archivo comprimido al usuario para descargarlo.
    # Utiliza el método 'send_file' de Flask y proporciona la ubicación del archivo comprimido.
    return send_file('compressed.zip', as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete():
    # Aquí debes eliminar el archivo comprimido del servidor.
    # Utiliza la función 'os.remove' de Python para eliminar el archivo.
    return {'message': 'Archivo comprimido eliminado.'}

if __name__ == '__main__':
    app.run()
