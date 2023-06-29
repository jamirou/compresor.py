$(document).ready(function() {
    $('#upload-form').submit(function(e) {
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

    $('#compress-btn').click(function() {
        $.ajax({
            url: '/compress',
            type: 'POST',
            beforeSend: function() {
                $('#loading').show();
            },
            success: function(response) {
                $('#loading').hide();
                $('#download-link').show();
                $('#delete-btn').show();
                $('#download-btn').attr('href', response.download_url);
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
            }
        });
    });
});
