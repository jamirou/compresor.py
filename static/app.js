$(document).ready(function() {
    $('#file-input').change(function(e) {
        e.preventDefault();
        var fileInput = document.getElementById('file-input');
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);

        // Envío de la solicitud POST al backend para cargar el archivo
        $.ajax({
            url: '/upload', // Ruta en el backend que manejará la carga del archivo
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
                $('#loading').show();
            },
            success: function(response) {
                $('#compress-btn').prop('disabled', false);
                $('#loading').hide();
                if (response.message) {
                    $('#success-message').text(response.message);
                    $('#success-message').show();
                    $('#error-message').hide();
                }
            },
            error: function(error) {
                $('#loading').hide();
                $('#success-message').hide(); // Ocultar el mensaje de éxito
                $('#error-message').text(error.responseJSON.message);
                $('#error-message').show();
            }
        });
    });

// Evento de clic para el botón "Comprimir Archivo"
$('#compress-btn').click(function() {
    // Mostrar el mensaje de carga
    $('#loading').show();
    // Deshabilitar el botón "Comprimir Archivo"
    $('#compress-btn').prop('disabled', true);
    // Obtener el archivo seleccionado
    var file = $('#file-input').prop('files')[0];
    // Crear un objeto FormData y agregar el archivo
    var formData = new FormData();
    formData.append('file', file);
    // Realizar una solicitud POST al endpoint '/compress'
    $.ajax({
        url: '/compress',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#loading').hide();
            if (response.message) {
                $('#success-message').text(response.message);
                $('#success-message').show();
            }
            // Mostrar el enlace de descarga proporcionado por el backend
            $('#download-link').show();
            $('#download-btn').attr('href', response.download_url);
            $('#download-btn').text('Download file');

            // Mostrar el botón "Eliminar Archivo Comprimido"
            $('#delete-btn').show();
        },
        error: function(error) {
            // Ocultar el mensaje de carga
            $('#loading').hide();

            // Mostrar el mensaje de error
            $('#error-message').text(error.responseJSON.message);
            $('#error-message').show();
        }
    });
});

    $('#delete-btn').click(function() {
        $.ajax({
            url: '/delete',
            type: 'POST',
            success: function(response) {
                $('#compress-btn').prop('disabled', true);
                $('#download-link').hide();
                $('#delete-btn').hide();
                // Limpiar el campo de entrada de archivos
                $('#file-input').val('');
                $('#success-message').hide();
            }
        });
    });
});