/**
 * Script para mostrar imágenes en la discografía
 */

async function loadDiscographyImages() {
    try {
        // Cargar información de discografía
        const response = await fetch('data/music/discography.json');
        const discography = await response.json();
        
        // Cargar información de la portada del EP
        const coverResponse = await fetch('data/media/covers/ep_cover_info.json');
        const coverInfo = await coverResponse.json();
        
        // Actualizar imágenes en la discografía
        updateDiscographyImages(discography, coverInfo);
        
        console.log('✅ Imágenes de discografía cargadas:', coverInfo);
        
    } catch (error) {
        console.error('❌ Error al cargar imágenes de discografía:', error);
    }
}

function updateDiscographyImages(discography, coverInfo) {
    // Buscar elementos de discografía en el DOM
    const discographySection = document.querySelector('.discography');
    
    if (discographySection) {
        // Crear elementos de imagen para cada álbum
        discography.albums.forEach((album, index) => {
            if (album.title === coverInfo.ep_title) {
                // Crear elemento de imagen para el EP
                const albumElement = createAlbumElement(album, coverInfo);
                discographySection.appendChild(albumElement);
            }
        });
    }
}

function createAlbumElement(album, coverInfo) {
    const albumDiv = document.createElement('div');
    albumDiv.className = 'album-item';
    albumDiv.innerHTML = `
        <div class="album-cover">
            <img src="${coverInfo.cover_image}" 
                 alt="${coverInfo.cover_alt}" 
                 class="album-image"
                 onerror="this.src='data/media/covers/pepito-grillo-ep-cover.png'">
        </div>
        <div class="album-info">
            <h4 class="album-title">${album.title}</h4>
            <p class="album-year">${album.year}</p>
            <p class="album-type">${album.type}</p>
            <p class="album-songs">${coverInfo.songs_count} canciones</p>
            <a href="${album.spotify_url}" target="_blank" class="spotify-link">
                🎵 Escuchar en Spotify
            </a>
        </div>
    `;
    
    return albumDiv;
}

// Cargar cuando se carga la página
document.addEventListener('DOMContentLoaded', loadDiscographyImages);
