/**
 * Script para actualizar estadísticas de Spotify dinámicamente
 */

async function updateSpotifyStats() {
    try {
        // Cargar estadísticas desde el archivo JSON
        const response = await fetch('data/spotify_stats.json');
        const stats = await response.json();
        
        // Actualizar oyentes mensuales
        const monthlyListenersElement = document.querySelector('.stat-item:first-child .stat-number');
        if (monthlyListenersElement) {
            monthlyListenersElement.textContent = stats.monthly_listeners;
        }
        
        // Actualizar seguidores
        const followersElement = document.querySelector('.stat-item:last-child .stat-number');
        if (followersElement) {
            followersElement.textContent = stats.followers;
        }
        
        console.log('✅ Estadísticas de Spotify actualizadas:', stats);
        
        // Mostrar última actualización
        const lastUpdated = new Date(stats.last_updated).toLocaleString('es-ES');
        console.log(`📅 Última actualización: ${lastUpdated}`);
        
    } catch (error) {
        console.error('❌ Error al actualizar estadísticas de Spotify:', error);
    }
}

// Actualizar estadísticas cuando se carga la página
document.addEventListener('DOMContentLoaded', updateSpotifyStats);

// Actualizar cada 5 minutos
setInterval(updateSpotifyStats, 5 * 60 * 1000);
