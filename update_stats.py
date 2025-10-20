#!/usr/bin/env python3
"""
Script simple para actualizar estadísticas de Spotify
Actualiza el archivo JSON con los datos más recientes
"""

import json
from datetime import datetime

def update_stats():
    """
    Actualiza las estadísticas con los datos más recientes de Spotify
    """
    # Datos actuales de Spotify (obtenidos manualmente del perfil)
    stats = {
        "monthly_listeners": "28,596",
        "followers": "14,772", 
        "last_updated": datetime.now().isoformat(),
        "source": "https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa"
    }
    
    # Guardar en archivo JSON
    with open('data/spotify_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print("✅ Estadísticas actualizadas:")
    print(f"   - Oyentes mensuales: {stats['monthly_listeners']}")
    print(f"   - Seguidores: {stats['followers']}")
    print(f"   - Última actualización: {stats['last_updated']}")

if __name__ == "__main__":
    update_stats()
