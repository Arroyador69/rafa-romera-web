#!/usr/bin/env python3
"""
Script para configurar la imagen de portada del EP 'Me Lleve a la Luna'
"""

import os
import json

def setup_ep_cover():
    """
    Configura la imagen de portada del EP
    """
    
    # Información de la imagen de portada
    cover_info = {
        "ep_title": "Me Lleve a la Luna",
        "artist": "Rafa Romera", 
        "year": "2025",
        "spotify_url": "https://open.spotify.com/intl-es/album/0GvYb51pA6EU9ftcSMU1SR",
        "cover_image": "pepito-grillo-ep-cover.jpg",
        "cover_alt": "Portada del EP Me Lleve a la Luna - Pepito Grillo en la luna",
        "description": "Ilustración vintage de Pepito Grillo en la luna mirando hacia el pueblo",
        "songs_count": 6,
        "songs": [
            "Me Lleve a la Luna",
            "Vuelvo al Pueblo", 
            "Pepito Grillo",
            "Tal Vez Fuimos",
            "Sigo Sin Dormir",
            "No Me Olvido"
        ]
    }
    
    # Guardar información de la portada
    with open('data/media/covers/ep_cover_info.json', 'w', encoding='utf-8') as f:
        json.dump(cover_info, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuración de portada del EP creada:")
    print(f"   - EP: {cover_info['ep_title']}")
    print(f"   - Artista: {cover_info['artist']}")
    print(f"   - Año: {cover_info['year']}")
    print(f"   - Canciones: {cover_info['songs_count']}")
    print(f"   - Archivo esperado: {cover_info['cover_image']}")
    
    print("\n📝 Para completar la configuración:")
    print("   1. Coloca la imagen de Pepito Grillo en:")
    print("      data/media/covers/pepito-grillo-ep-cover.jpg")
    print("   2. La imagen debe ser JPG o PNG")
    print("   3. Tamaño recomendado: 300x300px o más")
    
    return cover_info

if __name__ == "__main__":
    setup_ep_cover()
