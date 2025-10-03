#!/usr/bin/env python3
"""
Script para descargar imágenes de Instagram
"""
import requests
import re
import os
from urllib.parse import urlparse
import time

def download_instagram_image(url, filename):
    """Descarga una imagen de Instagram"""
    try:
        # Headers para simular un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Hacer la petición
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Buscar la URL de la imagen en el HTML
        html_content = response.text
        
        # Patrones para encontrar la imagen
        patterns = [
            r'"display_url":"([^"]+)"',
            r'"url":"([^"]*\.jpg[^"]*)"',
            r'<meta property="og:image" content="([^"]+)"',
            r'"thumbnail_src":"([^"]+)"'
        ]
        
        image_url = None
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                # Tomar la primera coincidencia y limpiar la URL
                image_url = matches[0].replace('\\u0026', '&')
                break
        
        if not image_url:
            print(f"No se encontró imagen en {url}")
            return False
            
        print(f"Imagen encontrada: {image_url}")
        
        # Descargar la imagen
        img_response = requests.get(image_url, headers=headers, timeout=30)
        img_response.raise_for_status()
        
        # Guardar la imagen
        with open(filename, 'wb') as f:
            f.write(img_response.content)
            
        print(f"Imagen guardada como: {filename}")
        return True
        
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return False

def main():
    # URLs de Instagram
    instagram_urls = [
        "https://www.instagram.com/p/DOjJbPJjPUH/?hl=es",
        "https://www.instagram.com/p/DO5nx9MjAfD/?hl=es", 
        "https://www.instagram.com/p/DOYc5__jBGZ/?hl=es"
    ]
    
    # Crear directorio si no existe
    os.makedirs("data/media/events", exist_ok=True)
    
    # Descargar cada imagen
    for i, url in enumerate(instagram_urls, 1):
        filename = f"data/media/events/evento_{i}.jpg"
        print(f"\nDescargando imagen {i} de {len(instagram_urls)}...")
        success = download_instagram_image(url, filename)
        
        if success:
            print(f"✅ Imagen {i} descargada exitosamente")
        else:
            print(f"❌ Error descargando imagen {i}")
            
        # Pausa entre descargas
        time.sleep(2)
    
    print("\n🎉 Proceso completado!")

if __name__ == "__main__":
    main()
