document.addEventListener("DOMContentLoaded", function () {
    // Optionally add some interactive JS
    // E.g., auto hide flash messages after 5 seconds
    setTimeout(function() {
        var flashMessages = document.querySelectorAll('.alert-dismissible');
        flashMessages.forEach(function(msg) {
            var closeButton = msg.querySelector('.btn-close');
            if(closeButton) closeButton.click();
        });
    }, 5000);
});










