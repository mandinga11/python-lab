document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            // Cambiar el ícono (opcional)
            if (navMenu.classList.contains('active')) {
                menuToggle.innerHTML = '✕'; // Icono de cerrar
                menuToggle.setAttribute('aria-expanded', 'true');
            } else {
                menuToggle.innerHTML = '☰'; // Icono de hamburguesa
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Cerrar menú si se hace clic en un enlace (para SPAs o navegación en la misma página)
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    menuToggle.innerHTML = '☰';
                    menuToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    // Opcional: Resaltar enlace activo al hacer scroll (más avanzado)
    // Se necesita lógica para detectar en qué sección está el usuario
});