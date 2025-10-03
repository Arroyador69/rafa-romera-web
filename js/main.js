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

// Efecto de scroll para los botones del hero
window.addEventListener('scroll', function() {
    const heroButtons = document.querySelector('.hero-buttons');
    const heroContent = document.querySelector('.hero-content');
    const scrollY = window.scrollY;
    const windowHeight = window.innerHeight;
    
    if (heroButtons && heroContent) {
        // Calcular el porcentaje de scroll en la sección hero
        const scrollPercent = Math.min(scrollY / windowHeight, 1);
        
        // Mover los botones hacia arriba gradualmente (más pronunciado)
        const moveUp = scrollPercent * 300; // Mover hasta 300px hacia arriba
        heroButtons.style.transform = `translateY(-${moveUp}px)`;
        
        // Añadir opacidad gradual
        const opacity = Math.max(1 - scrollPercent * 0.6, 0.1);
        heroButtons.style.opacity = opacity;
        
        // Añadir efecto de escala sutil
        const scale = Math.max(1 - scrollPercent * 0.15, 0.85);
        heroButtons.style.transform += ` scale(${scale})`;
        
        // Mover el contenido del hero más hacia arriba
        const contentMoveUp = scrollPercent * 100; // Mover hasta 100px hacia arriba
        heroContent.style.transform = `translateY(-${contentMoveUp}px)`;
        
        // Añadir efecto parallax sutil al texto
        const textOpacity = Math.max(1 - scrollPercent * 0.3, 0.7);
        const title = heroContent.querySelector('h1');
        const subtitle = heroContent.querySelector('p');
        
        if (title) title.style.opacity = textOpacity;
        if (subtitle) subtitle.style.opacity = textOpacity;
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

            // Actualizar carrusel de canciones en discografía
            const songsTrack = document.querySelector('.songs-track');
            if (songsTrack && data.popular_songs) {
                songsTrack.innerHTML = '';
                
                // Duplicar las canciones para el efecto de carrusel infinito
                const songs = [...data.popular_songs, ...data.popular_songs];
                
                songs.forEach((song, index) => {
                    const songItem = document.createElement('div');
                    songItem.className = 'song-item';
                    songItem.innerHTML = `
                        <div class="song-image">
                            <img src="${song.image_url || 'data/media/photos/photo_10.jpg'}" alt="${song.title}">
                        </div>
                        <div class="song-info">
                            <h4>${song.title}</h4>
                            <p>${song.plays ? song.plays.toLocaleString() + ' reproducciones' : 'Single'}</p>
                            <button class="play-button" onclick="window.open('${song.spotify_url || 'https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa'}', '_blank')">
                                <i class="fas fa-play"></i>
                                <span>Escuchar en Spotify</span>
                            </button>
                        </div>
                    `;
                    songsTrack.appendChild(songItem);
                });
                
                // Agregar efecto de desvanecimiento dinámico
                addFadeEffect();
            }

            // Actualizar discografía
            const albumsGrid = document.querySelector('.albums-grid');
            if (albumsGrid && data.albums) {
                albumsGrid.innerHTML = '';
                data.albums.forEach(album => {
                    const albumItem = document.createElement('div');
                    albumItem.className = 'album-item';
                    albumItem.innerHTML = `
                        <img src="${album.image_url || 'data/media/photos/photo_10.jpg'}" alt="${album.title}" class="album-cover">
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

// Función para agregar efecto de desvanecimiento a las canciones
function addFadeEffect() {
    const songsTrack = document.querySelector('.songs-track');
    const songsCarousel = document.querySelector('.songs-carousel');
    
    if (!songsTrack || !songsCarousel) return;
    
    function updateFadeEffect() {
        const carouselRect = songsCarousel.getBoundingClientRect();
        const songItems = songsTrack.querySelectorAll('.song-item');
        
        songItems.forEach(item => {
            const itemRect = item.getBoundingClientRect();
            const itemCenter = itemRect.left + itemRect.width / 2;
            const carouselLeft = carouselRect.left;
            const carouselRight = carouselRect.right;
            
            // Calcular opacidad basada en la posición
            let opacity = 1;
            
            // Fade out en los bordes
            if (itemCenter < carouselLeft + 100) {
                opacity = Math.max(0.3, (itemCenter - carouselLeft) / 100);
            } else if (itemCenter > carouselRight - 100) {
                opacity = Math.max(0.3, (carouselRight - itemCenter) / 100);
            }
            
            item.style.opacity = opacity;
            item.style.transition = 'opacity 0.3s ease';
        });
    }
    
    // Actualizar el efecto en scroll y resize
    window.addEventListener('scroll', updateFadeEffect);
    window.addEventListener('resize', updateFadeEffect);
    
    // Actualizar periódicamente durante la animación
    setInterval(updateFadeEffect, 100);
    
    // Inicializar
    updateFadeEffect();
}

// Funcionalidad del Lightbox
let currentImageIndex = 0;
const images = [
    'data/media/photos/photo_10.jpg',
    'data/media/photos/photo_6.jpg',
    'data/media/photos/photo_7.jpg',
    'data/media/photos/photo_8.jpg',
    'data/media/photos/photo_9.jpg',
    'data/media/photos/DSC02250.jpg',
    'data/media/photos/DSC02063.jpg',
    'data/media/photos/DSC02065.jpg',
    'data/media/photos/DSC02066.jpg',
    'data/media/photos/DSC02098-Editar-2.jpg',
    'data/media/photos/DSC02108-2.jpg',
    'data/media/photos/DSC02123.jpg',
    'data/media/photos/DSC02146.jpg',
    'data/media/photos/DSC02148.jpg',
    'data/media/photos/DSC02246.jpg',
    'data/media/photos/DSC02271-2.jpg',
    'data/media/photos/DSC02337.jpg',
    'data/media/photos/DSC02369.jpg',
    'data/media/photos/DSC02435.jpg',
    'data/media/photos/DSC02437.jpg',
    'data/media/photos/DSC02437-2.jpg',
    'data/media/photos/DSC02438.jpg',
    'data/media/photos/DSC02458.jpg',
    'data/media/photos/IMG_5507.JPG',
    'data/media/photos/IMG_5508.JPG',
    'data/media/photos/PHOTO-2025-06-05-10-05-21.jpg',
    'data/media/photos/PHOTO-2025-06-05-10-05-22.jpg',
    'data/media/photos/PHOTO-2025-06-05-10-05-22 2.jpg',
    'data/media/photos/PHOTO-2025-06-05-10-05-23.jpg'
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

 