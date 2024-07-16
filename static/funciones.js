 const Toast = Swal.mixin({
            toast: true,
            position: "bottom-end",
            showConfirmButton: false,
            timer: 4000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            }
        });

        function alertaSuccess(mensaje, time = 5000) {
            Toast.fire({
                icon: 'success',
                title: mensaje,
                timer: time
            });
        }

        function alertaWarning(mensaje, time = 5000) {
            Toast.fire({
                icon: 'warning',
                title: mensaje,
                timer: time
            });
        }

        function alertaDanger(mensaje, time = 5000) {
            Toast.fire({
                icon: 'error',
                title: mensaje,
                timer: time
            });
        }

        function alertaInfo(mensaje, time = 5000) {
            Toast.fire({
                icon: 'info',
                title: mensaje,
                timer: time
            });
        }