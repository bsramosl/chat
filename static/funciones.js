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

