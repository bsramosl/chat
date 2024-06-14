        function alertaSuccess(mensaje, time = 5000) {
            Swal.fire({
                toast: true,
                position: 'bottom',
                icon: 'success',
                title: mensaje,
                showConfirmButton: false,
                timer: time
            })
        }

        function alertaWarning(mensaje, time = 5000) {
            Swal.fire({
                toast: true,
                position: 'bottom',
                icon: 'warning',
                title: mensaje,
                showConfirmButton: false,
                timer: time
            })
        }

        function alertaDanger(mensaje, time = 5000) {
            Swal.fire({
                toast: true,
                position: 'bottom',
                icon: 'error',
                title: mensaje,
                showConfirmButton: false,
                timer: time
            })
        }

        function alertaInfo(mensaje, time = 5000) {
            Swal.fire({
                toast: true,
                position: 'bottom',
                icon: 'info',
                title: mensaje,
                showConfirmButton: false,
                timer: time
            })
        }

     function eliminarajax(pk, nombre, accion, url = '{{ request.path }}', titulo = 'Estás por eliminar este registro:') {
            Swal.fire({
                html: `<b>${titulo}</b> ${nombre}`,
                text: "Esta acción es irreversible",
                icon: 'info',
                showCancelButton: true,
                allowOutsideClick: false,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Si, deseo hacerlo',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                    //bloquearpantalla();
                    $.ajax({
                        type: 'POST',
                        url: '{{ reques.path }}',
                        async: false,
                        data: {
                            csrfmiddlewaretoken: '{{ csrf_token }}',
                            action: accion,
                            id: pk,
                        },
                        dataType: "json",
                        beforeSend: function () {
                            //bloquearpantalla();
                        }
                    }).done(function (data) {
                        $.unblockUI;
                        if (data.error === false) {
                            location.reload();
                        } else {
                            alertaDanger(data.message)
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        setTimeout($.unblockUI, 1);
                        alertaDanger('Error en el servidor', 'Advertencia!', 10000);
                    }).always(function () {
                    });
                } else {
                }
            })
        }