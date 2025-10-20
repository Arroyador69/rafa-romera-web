#!/usr/bin/env python3
"""
Script para limpiar la discografía y dejar solo los álbumes reales,
no las canciones individuales que deben estar solo en el carrusel
"""

import json

def clean_discography():
    """
    Limpia la sección de álbumes para que solo muestre álbumes reales,
    no canciones individuales
    """
    
    # Leer el archivo actual
    with open('data/music/discography.json', 'r', encoding='utf-8') as f:
        discography = json.load(f)
    
    # Definir los álbumes reales (no canciones individuales)
    real_albums = [
        {
            "title": "Me Lleve a la Luna",
            "year": 2025,
            "type": "EP",
            "spotify_url": "https://open.spotify.com/intl-es/album/0GvYb51pA6EU9ftcSMU1SR",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "total_songs": 6,
            "duration": "19 min 48 sec"
        },
        {
            "title": "En el Aire",
            "year": 2023,
            "type": "Album",
            "spotify_url": "https://open.spotify.com/album/0",
            "image_url": "https://i.scdn.co/image/ab67616d0000b273g7h8i9j0k1l2m3n4o5p6q7"
        }
    ]
    
    # Actualizar solo con álbumes reales
    discography["albums"] = real_albums
    
    # Mantener todas las canciones en popular_songs para el carrusel
    print("✅ Discografía limpiada:")
    print(f"   - Álbumes reales: {len(real_albums)}")
    print(f"   - Canciones en carrusel: {len(discography['popular_songs'])}")
    
    for album in real_albums:
        print(f"   📀 {album['title']} ({album['year']}) - {album['type']}")
    
    # Guardar el archivo actualizado
    with open('data/music/discography.json', 'w', encoding='utf-8') as f:
        json.dump(discography, f, indent=4, ensure_ascii=False)
    
    print("\n🎵 Canciones que permanecen en el carrusel:")
    for song in discography["popular_songs"]:
        print(f"   🎶 {song['title']} ({song['year']}) - {song['plays']:,} reproducciones")
    
    return discography

if __name__ == "__main__":
    clean_discography()
