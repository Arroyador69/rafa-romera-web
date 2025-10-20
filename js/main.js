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
        
        const name = document.getElementById('contactName').value;
        const email = document.getElementById('contactEmail').value;
        const message = document.getElementById('contactMessage').value;
        const statusDiv = document.getElementById('formStatus');
        
        // Mostrar estado de carga
        statusDiv.innerHTML = '<p style="color: #007bff;">Enviando mensaje...</p>';
        
        // Crear enlace mailto con todos los datos
        const subject = encodeURIComponent(`Mensaje desde la web de Rafa Romera - ${name}`);
        const body = encodeURIComponent(`Nombre: ${name}\nEmail: ${email}\n\nMensaje:\n${message}`);
        const mailtoLink = `mailto:erreshopping@gmail.com?subject=${subject}&body=${body}`;
        
        // Abrir cliente de email
        window.location.href = mailtoLink;
        
        // Mostrar mensaje de éxito
        setTimeout(() => {
            statusDiv.innerHTML = '<p style="color: #28a745;">¡Mensaje preparado! Se abrirá tu cliente de email para enviarlo.</p>';
            contactForm.reset();
        }, 1000);
        
        // Limpiar mensaje después de 5 segundos
        setTimeout(() => {
            statusDiv.innerHTML = '';
        }, 5000);
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
            console.log('🎵 Carrusel - songsTrack encontrado:', !!songsTrack);
            console.log('🎵 Carrusel - popular_songs:', data.popular_songs?.length);
            
            if (songsTrack && data.popular_songs) {
                songsTrack.innerHTML = '';
                
                // Duplicar las canciones para el efecto de carrusel infinito
                const songs = [...data.popular_songs, ...data.popular_songs];
                console.log('🎵 Carrusel - Total canciones a mostrar:', songs.length);
                
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
                            ${song.duration ? `<p class="song-duration">${song.duration}</p>` : ''}
                            ${song.featured_artist ? `<p class="featured-artist">(con ${song.featured_artist})</p>` : ''}
                            <button class="play-button" onclick="window.open('${song.spotify_url || 'https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa'}', '_blank')">
                                <i class="fas fa-play"></i>
                                <span>Escuchar en Spotify</span>
                            </button>
                        </div>
                    `;
                    songsTrack.appendChild(songItem);
                });
                
                console.log('🎵 Carrusel - Elementos creados:', songsTrack.children.length);
                
                // Agregar efecto de desvanecimiento dinámico
                addFadeEffect();
            } else {
                console.log('❌ Carrusel - No se pudo inicializar:', {
                    songsTrack: !!songsTrack,
                    popular_songs: !!data.popular_songs
                });
            }

            // La discografía ahora está vacía - todas las canciones van en el carrusel
            // No generar contenido en la sección de discografía

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
    
    // Inicializar galería
    initGallery();
    
    // Agregar navegación con teclado
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            previousGalleryImages();
        } else if (e.key === 'ArrowRight') {
            nextGalleryImages();
        }
    });
    
    // Inicializar menú hamburguesa
    initMobileMenu();
    
        // Los posts de Instagram se cargan automáticamente con el script de Instagram
});

// Función para manejar el menú móvil
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (!hamburger || !navLinks) return;
    
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
    
    // Cerrar menú al hacer clic en un enlace
    const navLinksItems = navLinks.querySelectorAll('a');
    navLinksItems.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });
}

// Funciones de la galería
function initGallery() {
    const galleryTrack = document.getElementById('galleryTrack');
    const galleryIndicators = document.getElementById('galleryIndicators');
    
    if (!galleryTrack || !galleryIndicators) return;
    
    // Limpiar contenido existente
    galleryTrack.innerHTML = '';
    galleryIndicators.innerHTML = '';
    
    // Crear elementos de imagen (duplicar para bucle infinito)
    const duplicatedImages = [...galleryImages, ...galleryImages, ...galleryImages];
    
    duplicatedImages.forEach((imageSrc, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        galleryItem.onclick = () => openLightbox(index % galleryImages.length);
        
        const img = document.createElement('img');
        img.src = imageSrc;
        img.alt = `Rafa Romera ${(index % galleryImages.length) + 1}`;
        
        galleryItem.appendChild(img);
        galleryTrack.appendChild(galleryItem);
    });
    
    // Crear indicadores (solo para las imágenes originales)
    const totalPages = Math.ceil(galleryImages.length / 4);
    for (let i = 0; i < totalPages; i++) {
        const indicator = document.createElement('div');
        indicator.className = `gallery-indicator ${i === 0 ? 'active' : ''}`;
        indicator.onclick = () => goToGalleryPage(i);
        galleryIndicators.appendChild(indicator);
    }
    
    // Posicionar en el centro (segundo conjunto de imágenes)
    currentGalleryPage = totalPages;
    updateGalleryView();
}

function updateGalleryView() {
    const galleryTrack = document.getElementById('galleryTrack');
    const indicators = document.querySelectorAll('.gallery-indicator');
    const prevBtn = document.querySelector('.gallery-prev');
    const nextBtn = document.querySelector('.gallery-next');
    
    if (!galleryTrack) return;
    
    // Calcular desplazamiento
    const itemWidth = galleryTrack.children[0]?.offsetWidth || 0;
    const gap = 20;
    const translateX = -(currentGalleryPage * 4 * (itemWidth + gap));
    
    galleryTrack.style.transform = `translateX(${translateX}px)`;
    
    // Calcular página actual para indicadores (modo bucle)
    const totalPages = Math.ceil(galleryImages.length / 4);
    const currentIndicatorPage = currentGalleryPage % totalPages;
    
    // Actualizar indicadores
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentIndicatorPage);
    });
    
    // Los botones nunca se deshabilitan en modo infinito
    if (prevBtn) {
        prevBtn.disabled = false;
    }
    if (nextBtn) {
        nextBtn.disabled = false;
    }
}

function previousGalleryImages() {
    currentGalleryPage--;
    updateGalleryView();
    
    // Resetear posición si llegamos al principio
    const totalPages = Math.ceil(galleryImages.length / 4);
    if (currentGalleryPage < 0) {
        setTimeout(() => {
            currentGalleryPage = totalPages * 2 - 1;
            updateGalleryView();
        }, 500);
    }
}

function nextGalleryImages() {
    currentGalleryPage++;
    updateGalleryView();
    
    // Resetear posición si llegamos al final
    const totalPages = Math.ceil(galleryImages.length / 4);
    if (currentGalleryPage >= totalPages * 3) {
        setTimeout(() => {
            currentGalleryPage = totalPages;
            updateGalleryView();
        }, 500);
    }
}

function goToGalleryPage(page) {
    const totalPages = Math.ceil(galleryImages.length / 4);
    if (page >= 0 && page < totalPages) {
        currentGalleryPage = totalPages + page;
        updateGalleryView();
    }
}

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

// Funcionalidad de la Galería
let currentGalleryPage = 0;
let galleryImages = [
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

// Funcionalidad del Lightbox
let currentImageIndex = 0;
const images = galleryImages;

function openLightbox(index) {
    currentImageIndex = index;
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCounter = document.getElementById('lightbox-counter');
    
    // Forzar estilos inline para asegurar que se apliquen
    lightboxImage.style.width = '500px';
    lightboxImage.style.height = '375px';
    lightboxImage.style.maxWidth = '500px';
    lightboxImage.style.maxHeight = '375px';
    lightboxImage.style.minWidth = '500px';
    lightboxImage.style.minHeight = '375px';
    lightboxImage.style.objectFit = 'cover';
    lightboxImage.style.display = 'block';
    lightboxImage.style.margin = '0 auto';
    
    lightboxImage.src = images[index];
    lightboxCounter.textContent = `${index + 1} / ${images.length}`;
    
    // Asegurar que los estilos se mantengan cuando la imagen se carga
    lightboxImage.onload = function() {
        this.style.width = '500px';
        this.style.height = '375px';
        this.style.maxWidth = '500px';
        this.style.maxHeight = '375px';
        this.style.minWidth = '500px';
        this.style.minHeight = '375px';
        this.style.objectFit = 'cover';
        this.style.display = 'block';
        this.style.margin = '0 auto';
    };
    
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
    
    // Forzar que la imagen se recargue y aplique los estilos
    lightboxImage.src = '';
    lightboxImage.style.width = '500px';
    lightboxImage.style.height = '375px';
    lightboxImage.style.maxWidth = '500px';
    lightboxImage.style.maxHeight = '375px';
    lightboxImage.style.minWidth = '500px';
    lightboxImage.style.minHeight = '375px';
    lightboxImage.style.objectFit = 'cover';
    
    // Pequeño delay para asegurar que se apliquen los estilos
    setTimeout(() => {
        lightboxImage.src = images[currentImageIndex];
        lightboxCounter.textContent = `${currentImageIndex + 1} / ${images.length}`;
        
        // Asegurar que los estilos se mantengan cuando la imagen se carga
        lightboxImage.onload = function() {
            this.style.width = '500px';
            this.style.height = '375px';
            this.style.maxWidth = '500px';
            this.style.maxHeight = '375px';
            this.style.minWidth = '500px';
            this.style.minHeight = '375px';
            this.style.objectFit = 'cover';
            this.style.display = 'block';
            this.style.margin = '0 auto';
        };
    }, 50);
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

// Los posts de Instagram se cargan automáticamente con el script de Instagram

 