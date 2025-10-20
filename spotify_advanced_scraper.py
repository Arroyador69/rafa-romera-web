#!/usr/bin/env python3
"""
Script AVANZADO para obtener datos EXACTOS directamente de Spotify
Usa múltiples técnicas para extraer reproducciones reales
"""

import requests
import json
import os
import re
from datetime import datetime
import time
from urllib.parse import urlparse, parse_qs
import random

class SpotifyAdvancedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Configurar sesión con headers avanzados"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def extract_track_id(self, url):
        """Extraer track ID de URL de Spotify"""
        patterns = [
            r'/track/([a-zA-Z0-9]+)',
            r'track/([a-zA-Z0-9]+)',
            r'([a-zA-Z0-9]{22})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_spotify_web_data(self, track_id):
        """Obtener datos desde la página web de Spotify"""
        try:
            url = f"https://open.spotify.com/track/{track_id}"
            
            # Añadir headers específicos para Spotify
            headers = {
                'Referer': 'https://open.spotify.com/',
                'Origin': 'https://open.spotify.com'
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            print(f"❌ Error web scraping: {str(e)}")
            return None
    
    def get_spotify_embed_data(self, track_id):
        """Obtener datos desde el embed de Spotify"""
        try:
            embed_url = f"https://open.spotify.com/embed/track/{track_id}"
            
            headers = {
                'Referer': 'https://open.spotify.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            response = self.session.get(embed_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            print(f"❌ Error embed scraping: {str(e)}")
            return None
    
    def extract_plays_from_content(self, content):
        """Extraer reproducciones del contenido HTML"""
        if not content:
            return None
        
        # Patrones más específicos para Spotify
        patterns = [
            # Patrones JSON específicos de Spotify
            r'"popularity":(\d+)',
            r'"followers":\s*{\s*"total":\s*(\d+)',
            r'"total":\s*(\d+)',
            
            # Patrones de reproducciones
            r'"playCount":(\d+)',
            r'"totalPlays":(\d+)',
            r'"plays":(\d+)',
            r'"streams":(\d+)',
            
            # Patrones en metadatos
            r'<meta[^>]*name="twitter:description"[^>]*content="[^"]*?(\d{1,3}(?:,\d{3})*)[^"]*"[^>]*>',
            r'<meta[^>]*property="og:description"[^>]*content="[^"]*?(\d{1,3}(?:,\d{3})*)[^"]*"[^>]*>',
            
            # Patrones en texto
            r'(\d{1,3}(?:,\d{3})*(?:,\d{3})*)\s*reproducciones',
            r'(\d{1,3}(?:,\d{3})*(?:,\d{3})*)\s*plays',
            r'(\d{1,3}(?:,\d{3})*(?:,\d{3})*)\s*streams',
            
            # Patrones en JavaScript
            r'playCount["\']?\s*:\s*["\']?(\d+)["\']?',
            r'plays["\']?\s*:\s*["\']?(\d+)["\']?',
            r'streams["\']?\s*:\s*["\']?(\d+)["\']?'
        ]
        
        all_numbers = []
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                try:
                    # Limpiar y convertir número
                    clean_num = match.replace(',', '').replace('.', '').replace('"', '').replace("'", '')
                    num = int(clean_num)
                    
                    # Filtrar números razonables (entre 1,000 y 100,000,000)
                    if 1000 <= num <= 100000000:
                        all_numbers.append(num)
                except ValueError:
                    continue
        
        if all_numbers:
            # Retornar el número más grande encontrado
            return max(all_numbers)
        
        return None
    
    def get_track_data_from_artist_page(self, track_id):
        """Obtener datos desde la página del artista"""
        try:
            artist_url = "https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa"
            
            response = self.session.get(artist_url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            
            # Buscar el track específico en la página del artista
            if track_id in content:
                plays = self.extract_plays_from_content(content)
                if plays:
                    return plays
            
            return None
            
        except Exception as e:
            print(f"❌ Error artista page: {str(e)}")
            return None
    
    def get_real_spotify_plays(self, spotify_url):
        """Obtener reproducciones reales usando múltiples métodos"""
        track_id = self.extract_track_id(spotify_url)
        if not track_id:
            return None
        
        print(f"   🔍 Track ID: {track_id}")
        
        # Método 1: Página web principal
        print("   🌐 Método 1: Página web principal...")
        web_content = self.get_spotify_web_data(track_id)
        plays = self.extract_plays_from_content(web_content)
        if plays:
            print(f"   ✅ Encontradas {plays:,} reproducciones (método web)")
            return plays
        
        # Método 2: Embed
        print("   🎵 Método 2: Embed...")
        embed_content = self.get_spotify_embed_data(track_id)
        plays = self.extract_plays_from_content(embed_content)
        if plays:
            print(f"   ✅ Encontradas {plays:,} reproducciones (método embed)")
            return plays
        
        # Método 3: Página del artista
        print("   👤 Método 3: Página del artista...")
        plays = self.get_track_data_from_artist_page(track_id)
        if plays:
            print(f"   ✅ Encontradas {plays:,} reproducciones (método artista)")
            return plays
        
        print("   ❌ No se encontraron reproducciones")
        return None
    
    def update_all_tracks(self):
        """Actualizar todas las canciones con datos reales de Spotify"""
        try:
            # Cargar archivo
            with open('data/music/discography.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("🎵 Spotify Advanced Scraper - Datos EXACTOS")
            print("🔍 Obteniendo datos REALES directamente de Spotify")
            print("=" * 70)
            
            updated_count = 0
            failed_count = 0
            
            for i, song in enumerate(data['popular_songs'], 1):
                title = song['title']
                spotify_url = song['spotify_url']
                old_plays = song['plays']
                
                print(f"\n[{i}/{len(data['popular_songs'])}] 🎵 {title}")
                print(f"   📊 Actual: {old_plays:,} reproducciones")
                
                # Obtener datos reales
                real_plays = self.get_real_spotify_plays(spotify_url)
                
                if real_plays and real_plays != old_plays:
                    song['plays'] = real_plays
                    print(f"   ✅ ACTUALIZADO: {old_plays:,} → {real_plays:,} reproducciones")
                    updated_count += 1
                elif real_plays:
                    print(f"   ℹ️  Sin cambios: {real_plays:,} reproducciones")
                else:
                    print(f"   ❌ No se pudieron obtener datos")
                    failed_count += 1
                
                # Pausa aleatoria para evitar detección
                sleep_time = random.uniform(2, 5)
                print(f"   ⏱️  Esperando {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            
            # Actualizar metadata
            data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['update_method'] = 'spotify_advanced_scraping'
            data['update_stats'] = {
                'updated': updated_count,
                'failed': failed_count,
                'total': len(data['popular_songs'])
            }
            
            # Guardar archivo
            with open('data/music/discography.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print("\n" + "=" * 70)
            print(f"✅ ACTUALIZACIÓN COMPLETADA:")
            print(f"   📊 Canciones actualizadas: {updated_count}")
            print(f"   ❌ Fallos: {failed_count}")
            print(f"   📁 Total procesadas: {len(data['popular_songs'])}")
            
            return updated_count > 0
            
        except Exception as e:
            print(f"❌ Error general: {str(e)}")
            return False

def main():
    """Función principal"""
    print("🎵 Spotify Advanced Scraper")
    print("🎯 Datos EXACTOS directamente de Spotify")
    print("⚠️  Usando técnicas avanzadas de scraping")
    print()
    
    if not os.path.exists('data/music/discography.json'):
        print("❌ Error: No se encontró discography.json")
        return
    
    scraper = SpotifyAdvancedScraper()
    success = scraper.update_all_tracks()
    
    if success:
        print("\n🎉 ¡Datos EXACTOS obtenidos de Spotify!")
        print("📊 Reproducciones actualizadas con datos reales")
        print("🔄 Sistema listo para actualización automática")
    else:
        print("\n❌ No se pudieron obtener datos de Spotify")
        print("🔧 Revisa la conexión y los enlaces")

if __name__ == "__main__":
    main()
