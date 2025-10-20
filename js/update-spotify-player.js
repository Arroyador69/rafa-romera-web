/**
 * Script para actualizar el reproductor de Spotify con las nuevas canciones del EP
 */

async function updateSpotifyPlayer() {
    try {
        // Cargar información del EP
        const response = await fetch('data/latest_ep.json');
        const epData = await response.json();
        
        // Actualizar el reproductor flotante si existe
        const floatingPlayer = document.getElementById('floatingPlayer');
        if (floatingPlayer) {
            // Actualizar el título del reproductor
            const playerHeader = floatingPlayer.querySelector('.floating-player-header span');
            if (playerHeader) {
                playerHeader.textContent = `🎵 ${epData.title} - ${epData.artist}`;
            }
        }
        
        // Crear lista de canciones del EP para mostrar
        const songsList = epData.songs.map((song, index) => 
            `${index + 1}. ${song.title} - ${song.artist}`
        ).join('\n');
        
        console.log('✅ Reproductor actualizado con el nuevo EP:');
        console.log(`📀 ${epData.title} (${epData.year})`);
        console.log(`🎵 ${epData.total_songs} canciones`);
        console.log(`⏱️ ${epData.duration}`);
        console.log('🎶 Canciones:', songsList);
        
    } catch (error) {
        console.error('❌ Error al actualizar reproductor de Spotify:', error);
    }
}

// Actualizar cuando se carga la página
document.addEventListener('DOMContentLoaded', updateSpotifyPlayer);
