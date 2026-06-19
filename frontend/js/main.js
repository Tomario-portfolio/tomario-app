document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(function (input) {
        if (!input.value) input.min = today;
    });

    const checkIn = document.getElementById('check_in');
    const checkOut = document.getElementById('check_out');
    if (checkIn && checkOut) {
        checkIn.addEventListener('change', function () {
            checkOut.min = checkIn.value;
            if (checkOut.value && checkOut.value <= checkIn.value) checkOut.value = '';
        });
    }
});
