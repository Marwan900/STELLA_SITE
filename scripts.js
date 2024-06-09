document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('section');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    sections.forEach(section => {
        observer.observe(section);
    });

    // Simulation de la réception des données
    setTimeout(() => {
        document.getElementById('temp-display').textContent = "23°C";
        document.getElementById('speed-display').textContent = "7.8 km/s / 0.01 g";
        document.getElementById('altitude-display').textContent = "408 km";
        document.getElementById('brightness-low-display').textContent = "Bas: 1.2 lx";
        document.getElementById('brightness-high-display').textContent = "Haut: 1200 lx";
    }, 2000);
});
