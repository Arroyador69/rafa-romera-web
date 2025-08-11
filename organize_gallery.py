#!/usr/bin/env python3
"""
Script para organizar las imágenes de la galería de Rafa Romera
Este script ayuda a organizar las 22 imágenes en la galería de manera inteligente.
"""

import os
import shutil
from pathlib import Path

def organize_gallery_images():
    """
    Organiza las imágenes de la galería proporcionando instrucciones
    para renombrar y organizar las 22 imágenes.
    """
    
    # Directorio de fotos
    photos_dir = Path("data/media/photos")
    
    # Verificar que el directorio existe
    if not photos_dir.exists():
        print(f"Error: El directorio {photos_dir} no existe.")
        return
    
    # Lista de imágenes actuales
    current_images = list(photos_dir.glob("photo_*.jpg"))
    current_images.sort()
    
    print(f"Imágenes actuales en el directorio: {len(current_images)}")
    for img in current_images:
        print(f"  - {img.name}")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES PARA ORGANIZAR LA GALERÍA")
    print("="*60)
    
    print("\n1. IMÁGENES ACTUALES (photo_1.jpg a photo_10.jpg):")
    print("   Estas imágenes ya están en el directorio y listas para usar.")
    
    print("\n2. IMÁGENES ADICIONALES NECESARIAS:")
    print("   Necesitas agregar las siguientes imágenes al directorio 'data/media/photos/':")
    
    missing_images = []
    for i in range(11, 23):  # photo_11.jpg a photo_22.jpg
        missing_images.append(f"photo_{i}.jpg")
    
    for img in missing_images:
        print(f"   - {img}")
    
    print("\n3. DESCRIPCIONES DE LAS IMÁGENES:")
    descriptions = [
        "🎤 CANTANDO EN VIVO - Imagen central de la web",
        "Retrato casual con camisa azul",
        "Retrato en estudio con fondo gris", 
        "Sonriendo con camisa a rayas",
        "Con chaqueta de cuero y puerta de madera",
        "Con guitarra clásica sentado",
        "Retrato pensativo con guitarra",
        "En habitación minimalista con cama",
        "De pie junto a la cama",
        "Sentado en la cama",
        "Retrato en silla amarilla",
        "Con camisa de rugby y jeans",
        "Con chaqueta denim y gorra",
        "Retrato en estudio con sombras dramáticas",
        "Con chaqueta de cuero en blanco y negro",
        "Sonriendo con chaqueta de cuero",
        "Retrato con tatuaje en el brazo",
        "Con suéter beige y logo BH",
        "Con chaqueta de cuero en calle urbana",
        "Con cardigan Lacoste y flores",
        "Retrato con tatuajes",
        "Retrato en silla amarilla pensativo",
        "Sonriendo con iluminación dramática"
    ]
    
    for i, desc in enumerate(descriptions, 1):
        print(f"   photo_{i:02d}.jpg: {desc}")
    
    print("\n4. PASOS PARA COMPLETAR LA GALERÍA:")
    print("   a) Copia las 12 imágenes adicionales al directorio 'data/media/photos/'")
    print("   b) Renombra las imágenes como photo_11.jpg, photo_12.jpg, etc.")
    print("   c) Asegúrate de que todas las imágenes tengan formato JPG")
    print("   d) Optimiza las imágenes para web (tamaño recomendado: 800x600px)")
    
    print("\n5. VERIFICACIÓN:")
    print("   Después de agregar las imágenes, ejecuta este script nuevamente")
    print("   para verificar que todas las 22 imágenes estén presentes.")
    
    # Verificar si todas las imágenes están presentes
    all_images = list(photos_dir.glob("photo_*.jpg"))
    all_images.sort()
    
    if len(all_images) == 22:
        print("\n✅ ¡Perfecto! Todas las 22 imágenes están presentes en la galería.")
        print("La galería está lista para usar.")
    else:
        print(f"\n⚠️  Faltan {22 - len(all_images)} imágenes para completar la galería.")
        print("Sigue las instrucciones anteriores para agregar las imágenes faltantes.")

def create_thumbnail_script():
    """
    Crea un script para generar miniaturas de las imágenes.
    """
    thumbnail_script = '''#!/usr/bin/env python3
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
'''
    
    with open("create_thumbnails.py", "w", encoding="utf-8") as f:
        f.write(thumbnail_script)
    
    print("\n6. SCRIPT DE MINIATURAS:")
    print("   Se ha creado 'create_thumbnails.py' para generar miniaturas.")
    print("   Ejecuta: python create_thumbnails.py")

if __name__ == "__main__":
    organize_gallery_images()
    create_thumbnail_script()
