// Wait for the window to load
window.addEventListener('load', function () {
    // Get the pre-loader and navbar elements
    var preloader = document.getElementById('preloader');
    var navbar = document.querySelector('.navbar');

    // Hide the navbar initially
    navbar.style.display = 'none';

    // Hide the pre-loader and show the navbar after a delay
    setTimeout(function() {
        preloader.style.opacity = '0'; // Fade out the pre-loader
        setTimeout(function() {
            preloader.style.zIndex = '0'; // Set z-index to 0 after fade-out
            preloader.style.opacity = '0'; // Set opacity to 0 after fade-out
            setTimeout(function() {
                preloader.style.display = 'none'; // Hide the pre-loader completely after fade-out and opacity/z-index set to 0
                navbar.style.display = 'block'; // Show the navbar
            }, .01); // Wait for 1 second after fade-out before hiding pre-loader
        }, 1000); // Wait for 1 second after fade-out before setting opacity/z-index to 0
    }, 2500); // Adjust the delay (in milliseconds) according to your video duration
});