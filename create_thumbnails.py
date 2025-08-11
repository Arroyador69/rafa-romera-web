#!/usr/bin/env python3
"""
Script para generar miniaturas de las imágenes de la galería
Requiere: pip install Pillow
"""

from PIL import Image
import os
from pathlib import Path

def create_thumbnails():
    photos_dir = Path("data/media/photos")
    thumbnails_dir = Path("data/media/thumbnails")
    
    # Crear directorio de miniaturas si no existe
    thumbnails_dir.mkdir(exist_ok=True)
    
    # Procesar todas las imágenes
    for img_path in photos_dir.glob("photo_*.jpg"):
        try:
            with Image.open(img_path) as img:
                # Crear miniatura de 300x300px
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                
                # Guardar miniatura
                thumbnail_path = thumbnails_dir / f"thumb_{img_path.name}"
                img.save(thumbnail_path, "JPEG", quality=85)
                print(f"Miniatura creada: {thumbnail_path}")
                
        except Exception as e:
            print(f"Error procesando {img_path}: {e}")

if __name__ == "__main__":
    create_thumbnails()
