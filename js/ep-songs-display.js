/**
 * Script para mostrar las canciones individuales del EP "Me Lleve a la Luna"
 */

async function displayEpSongs() {
    try {
        // Cargar información de discografía
        const response = await fetch('data/music/discography.json');
        const discography = await response.json();
        
        // Filtrar solo las canciones del EP
        const epSongs = discography.popular_songs.filter(song => 
            song.album === "Me Lleve a la Luna"
        );
        
        // Crear contenedor para las canciones del EP
        createEpSongsContainer(epSongs);
        
        console.log('✅ Canciones del EP cargadas:', epSongs.length);
        
    } catch (error) {
        console.error('❌ Error al cargar canciones del EP:', error);
    }
}

function createEpSongsContainer(songs) {
    // Buscar la sección de discografía
    const discographySection = document.querySelector('.discography');
    
    if (discographySection) {
        // Crear contenedor para las canciones del EP
        const epContainer = document.createElement('div');
        epContainer.className = 'ep-songs-container';
        epContainer.innerHTML = `
            <h3>🎵 EP "Me Lleve a la Luna" - Todas las Canciones</h3>
            <div class="ep-songs-grid">
                ${songs.map(song => createSongCard(song)).join('')}
            </div>
        `;
        
        // Insertar después del título de discografía
        const discographyTitle = discographySection.querySelector('h3');
        if (discographyTitle) {
            discographyTitle.insertAdjacentElement('afterend', epContainer);
        }
    }
}

function createSongCard(song) {
    const featuredArtist = song.featured_artist ? `<span class="featured-artist">(con ${song.featured_artist})</span>` : '';
    
    return `
        <div class="ep-song-card">
            <div class="song-image">
                <img src="data/media/covers/pepito-grillo-ep-cover.png" 
                     alt="Pepito Grillo - ${song.title}"
                     class="song-cover">
            </div>
            <div class="song-info">
                <h4 class="song-title">${song.title}</h4>
                ${featuredArtist}
                <p class="song-duration">${song.duration}</p>
                <p class="song-plays">${song.plays.toLocaleString()} reproducciones</p>
                <a href="${song.spotify_url}" target="_blank" class="spotify-play-button">
                    <i class="fab fa-spotify"></i> Escuchar en Spotify
                </a>
            </div>
        </div>
    `;
}

// Cargar cuando se carga la página
document.addEventListener('DOMContentLoaded', displayEpSongs);
