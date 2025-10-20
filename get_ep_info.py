#!/usr/bin/env python3
"""
Script para obtener información del nuevo EP "Me Lleve a la Luna" de Rafa Romera
"""

import json
from datetime import datetime

def get_ep_info():
    """
    Información del nuevo EP basada en los datos de Spotify
    """
    ep_info = {
        "title": "Me Lleve a la Luna",
        "artist": "Rafa Romera",
        "year": "2025",
        "type": "EP",
        "total_songs": 6,
        "duration": "19 min 48 sec",
        "spotify_url": "https://open.spotify.com/intl-es/album/0GvYb51pA6EU9ftcSMU1SR",
        "songs": [
            {
                "title": "Me Lleve a la Luna",
                "artist": "Rafa Romera",
                "duration": "3:15",
                "track_number": 1
            },
            {
                "title": "Vuelvo al Pueblo", 
                "artist": "Rafa Romera",
                "duration": "3:22",
                "track_number": 2
            },
            {
                "title": "Pepito Grillo",
                "artist": "Rafa Romera, Miguelichi López",
                "duration": "3:18",
                "track_number": 3
            },
            {
                "title": "Tal Vez Fuimos",
                "artist": "Rafa Romera", 
                "duration": "3:25",
                "track_number": 4
            },
            {
                "title": "Sigo Sin Dormir",
                "artist": "Rafa Romera",
                "duration": "3:12",
                "track_number": 5
            },
            {
                "title": "No Me Olvido",
                "artist": "Rafa Romera, Muerdo",
                "duration": "3:16",
                "track_number": 6
            }
        ],
        "last_updated": datetime.now().isoformat()
    }
    
    return ep_info

def save_ep_info():
    """
    Guarda la información del EP en un archivo JSON
    """
    ep_data = get_ep_info()
    
    # Guardar en archivo JSON
    with open('data/latest_ep.json', 'w', encoding='utf-8') as f:
        json.dump(ep_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Información del EP guardada:")
    print(f"   - Título: {ep_data['title']}")
    print(f"   - Año: {ep_data['year']}")
    print(f"   - Canciones: {ep_data['total_songs']}")
    print(f"   - Duración: {ep_data['duration']}")
    print(f"   - URL: {ep_data['spotify_url']}")
    
    return ep_data

if __name__ == "__main__":
    save_ep_info()
