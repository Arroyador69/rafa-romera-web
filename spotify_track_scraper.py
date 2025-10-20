#!/usr/bin/env python3
"""
Script para obtener reproducciones reales de canciones de Spotify
Actualiza automáticamente el archivo discography.json con datos reales
"""

import requests
import re
import json
import os
from datetime import datetime
import time

def get_track_plays(spotify_url):
    """
    Obtiene el número de reproducciones de una canción de Spotify
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(spotify_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        content = response.text
        
        # Patrones para encontrar reproducciones
        patterns = [
            r'"playCount":(\d+)',
            r'"plays":(\d+)',
            r'"totalPlays":(\d+)',
            r'(\d{1,3}(?:,\d{3})*(?:,\d{3})*)\s+plays',
            r'(\d{1,3}(?:\.\d{3})*(?:\.\d{3})*)\s+reproducciones',
            r'(\d{1,3}(?:,\d{3})*(?:,\d{3})*)\s+listens'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # Tomar el primer número encontrado
                play_count = matches[0].replace(',', '').replace('.', '')
                try:
                    return int(play_count)
                except ValueError:
                    continue
        
        # Si no encuentra reproducciones, buscar en metadatos
        meta_patterns = [
            r'<meta name="twitter:description" content="[^"]*?(\d{1,3}(?:,\d{3})*)[^"]*">',
            r'<meta property="og:description" content="[^"]*?(\d{1,3}(?:,\d{3})*)[^"]*">'
        ]
        
        for pattern in meta_patterns:
            matches = re.findall(pattern, content)
            if matches:
                play_count = matches[0].replace(',', '')
                try:
                    return int(play_count)
                except ValueError:
                    continue
        
        print(f"⚠️  No se pudieron obtener reproducciones para: {spotify_url}")
        return None
        
    except Exception as e:
        print(f"❌ Error al obtener reproducciones de {spotify_url}: {str(e)}")
        return None

def update_discography_plays():
    """
    Actualiza las reproducciones en el archivo discography.json
    """
    try:
        # Cargar el archivo actual
        with open('data/music/discography.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("🎵 Actualizando reproducciones de canciones...")
        
        # Actualizar canciones del EP
        ep_songs = [song for song in data['popular_songs'] if song.get('album') == 'Me Lleve a la Luna']
        print(f"📀 EP 'Me Lleve a la Luna': {len(ep_songs)} canciones")
        
        for song in ep_songs:
            print(f"🔄 Actualizando: {song['title']}")
            new_plays = get_track_plays(song['spotify_url'])
            if new_plays:
                old_plays = song['plays']
                song['plays'] = new_plays
                print(f"   ✅ {song['title']}: {old_plays:,} → {new_plays:,} reproducciones")
            else:
                print(f"   ⚠️  {song['title']}: No se pudo actualizar")
            
            # Pausa entre solicitudes para evitar rate limiting
            time.sleep(2)
        
        # Actualizar canciones populares
        popular_songs = [song for song in data['popular_songs'] if song.get('album') != 'Me Lleve a la Luna']
        print(f"🎶 Canciones populares: {len(popular_songs)} canciones")
        
        for song in popular_songs:
            print(f"🔄 Actualizando: {song['title']}")
            new_plays = get_track_plays(song['spotify_url'])
            if new_plays:
                old_plays = song['plays']
                song['plays'] = new_plays
                print(f"   ✅ {song['title']}: {old_plays:,} → {new_plays:,} reproducciones")
            else:
                print(f"   ⚠️  {song['title']}: No se pudo actualizar")
            
            # Pausa entre solicitudes
            time.sleep(2)
        
        # Actualizar timestamp
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar archivo actualizado
        with open('data/music/discography.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print("✅ Archivo discography.json actualizado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar discography.json: {str(e)}")
        return False

def main():
    """
    Función principal
    """
    print("🎵 Spotify Track Scraper - Actualizador de Reproducciones")
    print("=" * 60)
    
    if not os.path.exists('data/music/discography.json'):
        print("❌ Error: No se encontró el archivo data/music/discography.json")
        return
    
    success = update_discography_plays()
    
    if success:
        print("\n🎉 ¡Actualización completada exitosamente!")
        print("📊 Las reproducciones han sido actualizadas con datos reales de Spotify")
    else:
        print("\n❌ La actualización falló")
        print("🔧 Revisa los errores anteriores y vuelve a intentar")

if __name__ == "__main__":
    main()
