// Smooth scrolling para los enlaces de navegación
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animación del header al scroll
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
    } else {
        header.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    }
});

// Formulario de contacto
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Aquí iría la lógica para enviar el formulario
        // Por ahora solo mostramos un mensaje
        alert('Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.');
        contactForm.reset();
    });
}

// Cargar datos dinámicamente
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos de música desde el archivo JSON
    fetch('data/music/discography.json')
        .then(response => response.json())
        .then(data => {
            // Actualizar estadísticas del artista
            if (data.artist) {
                const statNumbers = document.querySelectorAll('.stat-number');
                if (statNumbers.length >= 2) {
                    statNumbers[0].textContent = data.artist.monthly_listeners.toLocaleString();
                    statNumbers[1].textContent = data.artist.followers.toLocaleString();
                }
            }

            // Actualizar canciones populares
            const songsGrid = document.querySelector('.songs-grid');
            if (songsGrid && data.popular_songs) {
                songsGrid.innerHTML = '';
                data.popular_songs.forEach(song => {
                    const songItem = document.createElement('div');
                    songItem.className = 'song-item';
                    songItem.innerHTML = `
                        <div class="song-info">
                            <h4>${song.title}</h4>
                            <p>${song.plays.toLocaleString()} reproducciones</p>
                            <span class="song-year">${song.year}</span>
                        </div>
                        <a href="https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa" target="_blank" class="spotify-link">
                            <i class="fab fa-spotify"></i> Escuchar
                        </a>
                    `;
                    songsGrid.appendChild(songItem);
                });
            }

            // Actualizar discografía
            const albumsGrid = document.querySelector('.albums-grid');
            if (albumsGrid && data.albums) {
                albumsGrid.innerHTML = '';
                data.albums.forEach(album => {
                    const albumItem = document.createElement('div');
                    albumItem.className = 'album-item';
                    albumItem.innerHTML = `
                        <div class="album-cover">
                            <i class="fas fa-music"></i>
                        </div>
                        <div class="album-info">
                            <h4>${album.title}</h4>
                            <p>${album.type} • ${album.year}</p>
                        </div>
                        <a href="https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa" target="_blank" class="album-link">
                            <i class="fab fa-spotify"></i>
                        </a>
                    `;
                    albumsGrid.appendChild(albumItem);
                });
            }

            // Actualizar últimos lanzamientos
            const releasesGrid = document.querySelector('.releases-grid');
            if (releasesGrid && data.singles) {
                releasesGrid.innerHTML = '';
                // Mostrar solo los últimos 3 singles
                const latestSingles = data.singles.slice(0, 3);
                latestSingles.forEach(single => {
                    const releaseItem = document.createElement('div');
                    releaseItem.className = 'release-item';
                    releaseItem.innerHTML = `
                        <div class="release-info">
                            <h4>${single.title}</h4>
                            <p>${single.type} • ${single.year}</p>
                        </div>
                        <a href="https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa" target="_blank" class="release-link">
                            <i class="fab fa-spotify"></i> Escuchar
                        </a>
                    `;
                    releasesGrid.appendChild(releaseItem);
                });
            }
        })
        .catch(error => console.error('Error al cargar la música:', error));

    // Cargar eventos desde el archivo JSON
    fetch('data/events/upcoming_events.json')
        .then(response => response.json())
        .then(data => {
            const eventsGrid = document.querySelector('.events-grid');
            if (eventsGrid && data.length > 0) {
                eventsGrid.innerHTML = '';
                data.forEach(event => {
                    const eventItem = document.createElement('div');
                    eventItem.className = 'event-item';
                    eventItem.innerHTML = `
                        <h3>${event.date}</h3>
                        <p>${event.venue}</p>
                        <p>${event.location}</p>
                        <a href="${event.link}" class="btn btn-primary" target="_blank">Comprar Entradas</a>
                    `;
                    eventsGrid.appendChild(eventItem);
                });
            }
        })
        .catch(error => console.error('Error al cargar los eventos:', error));
});

// Animación de elementos al scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Funcionalidad del reproductor flotante
function toggleFloatingPlayer() {
    const player = document.getElementById('floatingPlayer');
    player.classList.toggle('collapsed');
}

// Mostrar reproductor flotante después de 3 segundos
setTimeout(() => {
    const floatingPlayer = document.getElementById('floatingPlayer');
    if (floatingPlayer) {
        floatingPlayer.style.display = 'block';
        floatingPlayer.style.opacity = '0';
        floatingPlayer.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            floatingPlayer.style.transition = 'all 0.5s ease';
            floatingPlayer.style.opacity = '1';
            floatingPlayer.style.transform = 'translateY(0)';
        }, 100);
    }
}, 3000);

// Ocultar reproductor flotante inicialmente
document.addEventListener('DOMContentLoaded', function() {
    const floatingPlayer = document.getElementById('floatingPlayer');
    if (floatingPlayer) {
        floatingPlayer.style.display = 'none';
    }
});

// Funcionalidad del Lightbox
let currentImageIndex = 0;
const images = [
    'data/media/photos/photo_5.jpg',
    'data/media/photos/photo_6.jpg',
    'data/media/photos/photo_7.jpg',
    'data/media/photos/photo_8.jpg'
];

function openLightbox(index) {
    currentImageIndex = index;
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCounter = document.getElementById('lightbox-counter');
    
    lightboxImage.src = images[index];
    lightboxCounter.textContent = `${index + 1} / ${images.length}`;
    
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function changeImage(direction) {
    currentImageIndex = (currentImageIndex + direction + images.length) % images.length;
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCounter = document.getElementById('lightbox-counter');
    
    lightboxImage.src = images[currentImageIndex];
    lightboxCounter.textContent = `${currentImageIndex + 1} / ${images.length}`;
}

// Cerrar lightbox con ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLightbox();
    }
    
    // Navegar con flechas
    if (e.key === 'ArrowLeft') {
        const lightbox = document.getElementById('lightbox');
        if (lightbox.classList.contains('active')) {
            changeImage(-1);
        }
    }
    
    if (e.key === 'ArrowRight') {
        const lightbox = document.getElementById('lightbox');
        if (lightbox.classList.contains('active')) {
            changeImage(1);
        }
    }
});

 