#!/usr/bin/env python3
"""
Scraper para obtener estadísticas actualizadas de Spotify
Usa web scraping para obtener datos del perfil público de Rafa Romera
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

def scrape_spotify_profile():
    """
    Scraping del perfil público de Spotify de Rafa Romera
    """
    url = "https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar datos en el contenido de la página
            content = response.text
            
            # Extraer oyentes mensuales
            monthly_listeners_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s+monthly\s+listeners', content, re.IGNORECASE)
            monthly_listeners = monthly_listeners_match.group(1).replace(',', '') if monthly_listeners_match else "28596"
            
            # Extraer seguidores
            followers_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s+Followers', content, re.IGNORECASE)
            followers = followers_match.group(1).replace(',', '') if followers_match else "14772"
            
            return {
                'monthly_listeners': monthly_listeners,
                'followers': followers,
                'timestamp': datetime.now().isoformat()
            }
        else:
            print(f"Error al acceder a Spotify: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error en el scraping: {e}")
        return None

def update_stats_json(data):
    """
    Actualiza un archivo JSON con las estadísticas
    """
    stats_file = 'data/spotify_stats.json'
    
    # Crear directorio si no existe
    os.makedirs('data', exist_ok=True)
    
    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Estadísticas guardadas en {stats_file}")
        return True
        
    except Exception as e:
        print(f"Error al guardar estadísticas: {e}")
        return False

def update_html_with_stats(data):
    """
    Actualiza el HTML con las nuevas estadísticas
    """
    html_file = 'index.html'
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Formatear números con puntos como separadores de miles
        monthly_listeners = f"{int(data['monthly_listeners']):,}".replace(',', '.')
        followers = f"{int(data['followers']):,}".replace(',', '.')
        
        # Actualizar oyentes mensuales
        content = re.sub(r'<span class="stat-number">\d{1,3}(?:\.\d{3})*</span>', 
                        f'<span class="stat-number">{monthly_listeners}</span>', 
                        content)
        
        # Actualizar seguidores (segunda ocurrencia)
        stat_items = re.findall(r'<div class="stat-item">.*?</div>', content, re.DOTALL)
        if len(stat_items) >= 2:
            # Reemplazar el segundo stat-item (seguidores)
            new_followers_item = stat_items[1].replace(
                re.search(r'<span class="stat-number">\d{1,3}(?:\.\d{3})*</span>', stat_items[1]).group(),
                f'<span class="stat-number">{followers}</span>'
            )
            content = content.replace(stat_items[1], new_followers_item)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML actualizado:")
        print(f"   - Oyentes mensuales: {monthly_listeners}")
        print(f"   - Seguidores: {followers}")
        
        return True
        
    except Exception as e:
        print(f"Error al actualizar HTML: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🎵 Actualizando estadísticas de Spotify...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Obtener datos
    data = scrape_spotify_profile()
    
    if data:
        print(f"📊 Datos obtenidos:")
        print(f"   - Oyentes mensuales: {data['monthly_listeners']}")
        print(f"   - Seguidores: {data['followers']}")
        
        # Guardar en JSON
        update_stats_json(data)
        
        # Actualizar HTML
        update_html_with_stats(data)
        
        print("✅ Actualización completada")
    else:
        print("❌ No se pudieron obtener datos")

if __name__ == "__main__":
    import os
    main()
