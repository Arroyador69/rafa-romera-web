#!/usr/bin/env python3
"""
Script para descargar la imagen de portada del EP "Me Lleve a la Luna"
"""

import os
import json

def create_ep_cover_placeholder():
    """
    Crea un placeholder para la imagen de portada del EP
    Ya que no podemos descargar directamente desde Spotify sin API,
    crearemos un archivo de referencia
    """
    
    # Información de la imagen de portada
    cover_info = {
        "ep_title": "Me Lleve a la Luna",
        "artist": "Rafa Romera", 
        "year": "2025",
        "spotify_url": "https://open.spotify.com/intl-es/album/0GvYb51pA6EU9ftcSMU1SR",
        "cover_image": "me-lleve-a-la-luna-cover.jpg",
        "cover_alt": "Portada del EP Me Lleve a la Luna de Rafa Romera",
        "note": "Para obtener la imagen real, visita el enlace de Spotify y descarga manualmente"
    }
    
    # Guardar información de la portada
    with open('data/ep_cover_info.json', 'w', encoding='utf-8') as f:
        json.dump(cover_info, f, indent=2, ensure_ascii=False)
    
    # Crear directorio para imágenes de discos si no existe
    os.makedirs('data/media/covers', exist_ok=True)
    
    print("✅ Información de portada creada:")
    print(f"   - EP: {cover_info['ep_title']}")
    print(f"   - Artista: {cover_info['artist']}")
    print(f"   - Año: {cover_info['year']}")
    print(f"   - Archivo esperado: {cover_info['cover_image']}")
    print(f"   - URL de Spotify: {cover_info['spotify_url']}")
    print("\n📝 Para obtener la imagen real:")
    print("   1. Ve al enlace de Spotify")
    print("   2. Descarga la imagen de portada")
    print("   3. Nómbrala como 'me-lleve-a-la-luna-cover.jpg'")
    print("   4. Colócala en 'data/media/covers/'")
    
    return cover_info

if __name__ == "__main__":
    create_ep_cover_placeholder()
