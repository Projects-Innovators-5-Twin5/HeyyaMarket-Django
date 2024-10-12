$(document).ready(function () {
    $('#editModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); 
        var url = button.data('url');
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',  
            success: function (data) {
                $('#modal-content-placeholder').html(data.form); 
                $('#editModal').modal('show'); 
            },
            error: function (xhr, status, error) {
                console.error("Erreur lors du chargement du modal: ", error);
            }
        });

        $(document).on('submit', 'form', function (event) {
            event.preventDefault(); 
            $('#alert-container').empty();
            var form = $(this);
            var actionUrl = form.attr('action');  
            $.ajax({
                type: 'POST',
                url: actionUrl,
                data: new FormData(this),  
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response.success) {
                        $('#alert-container').html(`
                            <div class="alert alert-success" role="alert">
                              ${response.message}
                            </div>
                        `);
                        $('#editModal').modal('hide');  
                        window.scrollTo({ top: 0, behavior: 'smooth' });

                       
                        setTimeout(function () {
                            location.reload();  
                        }, 3000);
                    } else {
                        $('#alert-container').html(`
                            <div class="alert alert-danger" role="alert">
                              ${response.message}
                            </div>
                        `);
                        window.scrollTo({ top: 0, behavior: 'smooth' });  

                    }
                },
                error: function (xhr, status, error) {
                    $('#alert-container').html(`
                        <div class="alert alert-danger" role="alert">
                          ${response.message}
                        </div>
                    `);
                    window.scrollTo({ top: 0, behavior: 'smooth' }); 
                }
            });
        });
    });
});
$(document).ready(function () {
    $('#deleteConfirmationModal').on('shown.bs.modal', function (event) {
        var button = $(event.relatedTarget); 
        var type = button.data('type'); 

        $('#type-placeholder').text(type);

        var deleteUrl = button.data('url'); 
        $('#delete-category-btn').off('click').on('click', function (event) {
            event.preventDefault(); 
            $.ajax({
                type: 'POST',
                url: deleteUrl,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function (response) {
                    if (response.success) {
                        $('#alert-container').html(`
                            <div class="alert alert-success" role="alert">
                                ${response.message}
                            </div>
                        `);
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                        $('#deleteConfirmationModal').modal('hide');  

                        setTimeout(function () {
                            location.reload();  
                        }, 3000); 
                    }
                    else {
                        alert('Erreur lors de la suppression de la catégorie.');
                    }
                },
                error: function (xhr) {
                    $('#alert-container').html(`
                        <div class="alert alert-danger" role="alert">
                            ${error.message}
                        </div>
                    `);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    $('#deleteConfirmationModal').modal('hide');  
                }
            });
        });
    });

    
});
$(document).ready(function() {
    $('#categoryForm').on('submit', function(e) {
        e.preventDefault(); 
        var formData = new FormData(this);
        var form = $(this);
        var actionUrl = form.attr('action');  
        $.ajax({
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    $('#alert-container').html(`
                        <div class="alert alert-success" role="alert">
                          ${response.message}
                        </div>
                    `);
                    $('#editModal').modal('hide');  
                    window.scrollTo({ top: 0, behavior: 'smooth' });

                   
                    setTimeout(function () {
                        location.reload();  
                    }, 3000);         
                   } else {
                    var errors = response.errors;
                    
                    var errorHtml = '<div class="alert alert-danger"><ul>';
                    $.each(errors, function(key, value) {
                        errorHtml += '<li>' + value[0] + '</li>';  // Adjust error display
                    });
                    errorHtml += '</ul></div>';
                    $('#alert-container').html(errorHtml);
                }
            },
            error: function(xhr, status, error) {
                $('#alert-container').html('<div class="alert alert-danger">An error occurred. Please try again.</div>');
            }
        });
    });
    $('#productForm').on('submit', function(e) {
        e.preventDefault(); 
        var formData = new FormData(this);
        var form = $(this);
        var actionUrl = form.attr('action');  
        $.ajax({
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    $('#alert-container').html(`
                        <div class="alert alert-success" role="alert">
                          ${response.message}
                        </div>
                    `);
                    $('#editModal').modal('hide');  
                    window.scrollTo({ top: 0, behavior: 'smooth' });

                   
                    setTimeout(function () {
                        location.reload();  
                    }, 3000);         
                   } else {
                    var errors = response.errors;
                    
                    var errorHtml = '<div class="alert alert-danger"><ul>';
                    $.each(errors, function(key, value) {
                        errorHtml += '<li>' + value[0] + '</li>';  // Adjust error display
                    });
                    errorHtml += '</ul></div>';
                    $('#alert-container').html(errorHtml);
                }
            },
            error: function(xhr, status, error) {
                $('#alert-container').html('<div class="alert alert-danger">An error occurred. Please try again.</div>');
            }
        });
    });
    $('#editProduitModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); 
        var url = button.data('url');
        console.log(url);
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',  
            success: function (data) {
                $('#modal-content-placeholder').html(data.form); 
                $('#editProduitModal').modal('show'); 
            },
            error: function (xhr, status, error) {
                console.error("Erreur lors du chargement du modal: ", error);
            }
        });

        $(document).on('submit', 'form', function (event) {
            event.preventDefault(); 
            $('#alert-container').empty();
            var form = $(this);
            var actionUrl = form.attr('action');  
            console.log(actionUrl);
            $.ajax({
                type: 'POST',
                url: actionUrl,
                data: new FormData(this),  
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response.success) {
                        $('#alert-container').html(`
                            <div class="alert alert-success" role="alert">
                              ${response.message}
                            </div>
                        `);
                        $('#editProduitModal').modal('hide');  
                        window.scrollTo({ top: 0, behavior: 'smooth' });
        
                        setTimeout(function () {
                            location.reload();  
                        }, 3000);
                    } else {
                        $('#alert-container').html(`
                            <div class="alert alert-danger" role="alert">
                              ${response.message}
                            </div>
                        `);
                        window.scrollTo({ top: 0, behavior: 'smooth' });  
                    }
                },
                error: function (xhr, status, error) {
                    $('#alert-container').html(`
                        <div class="alert alert-danger" role="alert">
                          Une erreur s'est produite lors de la mise à jour du produit.
                        </div>
                    `);
                    window.scrollTo({ top: 0, behavior: 'smooth' }); 
                }
            });
        });
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
