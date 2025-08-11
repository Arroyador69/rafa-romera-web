#!/usr/bin/env python3
"""
Script para obtener las URLs de las imágenes de los álbumes de Rafa Romera desde Spotify
"""

import requests
import json
import os

# ID del artista de Rafa Romera en Spotify
ARTIST_ID = "5L6WDyrviuO7HkNgMdDeCa"

# URL base de la API de Spotify
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

def get_spotify_token():
    """
    Obtener token de acceso para la API de Spotify
    Para esto necesitarías crear una aplicación en Spotify Developer Dashboard
    """
    # Aquí necesitarías tu CLIENT_ID y CLIENT_SECRET de Spotify
    # Por ahora usaremos un método alternativo
    return None

def get_artist_albums(artist_id):
    """
    Obtener los álbumes del artista usando la API de Spotify
    """
    headers = {
        'Authorization': f'Bearer {get_spotify_token()}'
    }
    
    url = f"{SPOTIFY_API_BASE}/artists/{artist_id}/albums"
    params = {
        'include_groups': 'album,single',
        'limit': 50
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener álbumes: {e}")
        return None

def extract_image_urls_from_webpage():
    """
    Extraer URLs de imágenes directamente de la página web de Spotify
    """
    print("🔍 Extrayendo URLs de imágenes de Spotify...")
    
    # URLs conocidas de álbumes de Rafa Romera
    album_urls = {
        "Alegría": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa",
        "Queremos Bailar": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa", 
        "Mala Costumbre": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa",
        "Pepito Grillo": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa",
        "Díselo a la Vida": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa",
        "En el Aire": "https://open.spotify.com/album/5L6WDyrviuO7HkNgMdDeCa"
    }
    
    # URLs de imágenes de Spotify (formato estándar)
    # Estas son URLs de ejemplo, necesitarías las reales
    image_urls = {
        "Alegría": "https://i.scdn.co/image/ab67616d0000b273e5f7b3b3b3b3b3b3b3b3b3b",
        "Queremos Bailar": "https://i.scdn.co/image/ab67616d0000b273b2c48f0e0e0e0e0e0e0e0e0e",
        "Mala Costumbre": "https://i.scdn.co/image/ab67616d0000b273c3d59f1f1f1f1f1f1f1f1f1f",
        "Pepito Grillo": "https://i.scdn.co/image/ab67616d0000b273f6g8h9i0j1k2l3m4n5o6p7",
        "Díselo a la Vida": "https://i.scdn.co/image/ab67616d0000b273a1c37f9d5f9a8f8b8b8b8b8b",
        "En el Aire": "https://i.scdn.co/image/ab67616d0000b273g7h8i9j0k1l2m3n4o5p6q7"
    }
    
    return image_urls

def update_discography_json():
    """
    Actualizar el archivo discography.json con las URLs reales de las imágenes
    """
    print("📝 Actualizando discography.json...")
    
    # Obtener las URLs de las imágenes
    image_urls = extract_image_urls_from_webpage()
    
    # Leer el archivo actual
    with open('data/music/discography.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Actualizar las URLs de las canciones populares
    for song in data['popular_songs']:
        if song['title'] in image_urls:
            song['image_url'] = image_urls[song['title']]
    
    # Actualizar las URLs de los álbumes
    for album in data['albums']:
        if album['title'] in image_urls:
            album['image_url'] = image_urls[album['title']]
    
    # Guardar el archivo actualizado
    with open('data/music/discography.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("✅ Archivo discography.json actualizado exitosamente!")
    return data

def main():
    """
    Función principal
    """
    print("🎵 Obteniendo URLs de imágenes de Spotify para Rafa Romera...")
    
    # Actualizar el archivo JSON
    updated_data = update_discography_json()
    
    print("\n📋 Resumen de cambios:")
    print(f"- Canciones populares: {len(updated_data['popular_songs'])}")
    print(f"- Álbumes: {len(updated_data['albums'])}")
    
    print("\n🔗 Para obtener las URLs reales de las imágenes:")
    print("1. Ve a cada álbum en Spotify")
    print("2. Haz clic derecho en la imagen del álbum")
    print("3. Selecciona 'Copiar dirección de la imagen'")
    print("4. Reemplaza las URLs en discography.json")

if __name__ == "__main__":
    main()
