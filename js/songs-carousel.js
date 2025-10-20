/**
 * Script para el carrusel de canciones con bucle continuo y velocidad aumentada
 */

let songsCarouselInterval;
let currentSongIndex = 0;
let songsData = [];

// Función para inicializar el carrusel de canciones
async function initSongsCarousel() {
    try {
        // Cargar datos de música
        const response = await fetch('data/music/discography.json');
        const data = await response.json();
        
        songsData = data.popular_songs || [];
        
        if (songsData.length === 0) {
            console.warn('No hay canciones disponibles');
            return;
        }
        
        // Inicializar el carrusel
        setupSongsCarousel();
        
        // Iniciar el bucle automático
        startSongsCarousel();
        
        console.log(`✅ Carrusel de canciones inicializado con ${songsData.length} canciones`);
        
    } catch (error) {
        console.error('❌ Error al inicializar carrusel de canciones:', error);
    }
}

// Función para configurar el carrusel
function setupSongsCarousel() {
    const songsTrack = document.querySelector('.songs-track');
    const songsCarousel = document.querySelector('.songs-carousel');
    
    if (!songsTrack || !songsCarousel) {
        console.warn('Elementos del carrusel no encontrados');
        return;
    }
    
    // Limpiar contenido existente
    songsTrack.innerHTML = '';
    
    // Crear elementos de canciones (triplicar para bucle infinito)
    const tripledSongs = [...songsData, ...songsData, ...songsData];
    
    tripledSongs.forEach((song, index) => {
        const songItem = document.createElement('div');
        songItem.className = 'song-item';
        songItem.innerHTML = `
            <div class="song-image">
                <img src="${song.image_url || 'data/media/photos/photo_10.jpg'}" 
                     alt="${song.title}"
                     onerror="this.src='data/media/photos/photo_10.jpg'">
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
    
    // Posicionar en el segundo conjunto de canciones (para bucle infinito)
    const songItemWidth = songsTrack.children[0]?.offsetWidth || 300;
    const gap = 20;
    const translateX = -(songsData.length * (songItemWidth + gap));
    songsTrack.style.transform = `translateX(${translateX}px)`;
    songsTrack.style.transition = 'transform 0.5s ease';
    
    // Aplicar efecto de desvanecimiento
    applyFadeEffect();
}

// Función para iniciar el carrusel automático
function startSongsCarousel() {
    // Limpiar intervalo anterior si existe
    if (songsCarouselInterval) {
        clearInterval(songsCarouselInterval);
    }
    
    // Mover a la siguiente canción cada 3 segundos (más rápido que antes)
    songsCarouselInterval = setInterval(() => {
        moveToNextSong();
    }, 3000);
}

// Función para mover a la siguiente canción
function moveToNextSong() {
    const songsTrack = document.querySelector('.songs-track');
    if (!songsTrack || songsData.length === 0) return;
    
    currentSongIndex++;
    
    // Si llegamos al final del segundo conjunto, resetear al principio del segundo conjunto
    if (currentSongIndex >= songsData.length * 2) {
        currentSongIndex = songsData.length;
        
        // Resetear posición sin transición
        const songItemWidth = songsTrack.children[0]?.offsetWidth || 300;
        const gap = 20;
        const translateX = -(songsData.length * (songItemWidth + gap));
        songsTrack.style.transition = 'none';
        songsTrack.style.transform = `translateX(${translateX}px)`;
        
        // Restaurar transición en el siguiente frame
        requestAnimationFrame(() => {
            songsTrack.style.transition = 'transform 0.5s ease';
        });
        
        return;
    }
    
    // Mover al siguiente elemento
    const songItemWidth = songsTrack.children[0]?.offsetWidth || 300;
    const gap = 20;
    const translateX = -(currentSongIndex * (songItemWidth + gap));
    songsTrack.style.transform = `translateX(${translateX}px)`;
    
    // Aplicar efecto de desvanecimiento
    applyFadeEffect();
}

// Función para aplicar efecto de desvanecimiento
function applyFadeEffect() {
    const songsCarousel = document.querySelector('.songs-carousel');
    const songsTrack = document.querySelector('.songs-track');
    
    if (!songsCarousel || !songsTrack) return;
    
    const carouselRect = songsCarousel.getBoundingClientRect();
    const songItems = songsTrack.querySelectorAll('.song-item');
    
    songItems.forEach((item, index) => {
        const itemRect = item.getBoundingClientRect();
        const itemCenter = itemRect.left + itemRect.width / 2;
        const carouselCenter = carouselRect.left + carouselRect.width / 2;
        
        // Calcular distancia desde el centro
        const distance = Math.abs(itemCenter - carouselCenter);
        const maxDistance = carouselRect.width / 2;
        
        // Calcular opacidad basada en la distancia
        let opacity = 1 - (distance / maxDistance) * 0.8;
        opacity = Math.max(0.2, Math.min(1, opacity));
        
        // Aplicar escala para el elemento central
        let scale = 1;
        if (distance < 100) {
            scale = 1 + (1 - distance / 100) * 0.1;
        }
        
        item.style.opacity = opacity;
        item.style.transform = `scale(${scale})`;
        item.style.transition = 'all 0.3s ease';
    });
}

// Función para pausar el carrusel
function pauseSongsCarousel() {
    if (songsCarouselInterval) {
        clearInterval(songsCarouselInterval);
        songsCarouselInterval = null;
    }
}

// Función para reanudar el carrusel
function resumeSongsCarousel() {
    if (!songsCarouselInterval) {
        startSongsCarousel();
    }
}

// Pausar cuando el usuario interactúa con el carrusel
document.addEventListener('DOMContentLoaded', function() {
    const songsCarousel = document.querySelector('.songs-carousel');
    if (songsCarousel) {
        // Solo pausar con hover, no con clic
        songsCarousel.addEventListener('mouseenter', pauseSongsCarousel);
        songsCarousel.addEventListener('mouseleave', resumeSongsCarousel);
        
        // No pausar al hacer clic en botones de play
        // El carrusel continúa girando siempre
    }
});

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', initSongsCarousel);

// Exportar funciones para uso global
window.pauseSongsCarousel = pauseSongsCarousel;
window.resumeSongsCarousel = resumeSongsCarousel;
