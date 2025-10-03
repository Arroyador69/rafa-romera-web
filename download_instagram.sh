#!/bin/bash

# Crear directorio si no existe
mkdir -p data/media/events

echo "🎬 Descargando imágenes de Instagram..."

# URL 1 - Evento más próximo
echo "📥 Descargando evento 1..."
curl -s "https://www.instagram.com/p/DOjJbPJjPUH/?hl=es" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  | grep -o '"display_url":"[^"]*"' \
  | head -1 \
  | sed 's/"display_url":"//' \
  | sed 's/"//' \
  | sed 's/\\u0026/\&/g' \
  > temp_url1.txt

if [ -s temp_url1.txt ]; then
    IMAGE_URL1=$(cat temp_url1.txt)
    echo "🔗 URL encontrada: $IMAGE_URL1"
    curl -s "$IMAGE_URL1" -o "data/media/events/evento_1.jpg"
    echo "✅ Evento 1 descargado"
else
    echo "❌ No se pudo obtener la URL del evento 1"
fi

# URL 2
echo "📥 Descargando evento 2..."
curl -s "https://www.instagram.com/p/DO5nx9MjAfD/?hl=es" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  | grep -o '"display_url":"[^"]*"' \
  | head -1 \
  | sed 's/"display_url":"//' \
  | sed 's/"//' \
  | sed 's/\\u0026/\&/g' \
  > temp_url2.txt

if [ -s temp_url2.txt ]; then
    IMAGE_URL2=$(cat temp_url2.txt)
    echo "🔗 URL encontrada: $IMAGE_URL2"
    curl -s "$IMAGE_URL2" -o "data/media/events/evento_2.jpg"
    echo "✅ Evento 2 descargado"
else
    echo "❌ No se pudo obtener la URL del evento 2"
fi

# URL 3
echo "📥 Descargando evento 3..."
curl -s "https://www.instagram.com/p/DOYc5__jBGZ/?hl=es" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  | grep -o '"display_url":"[^"]*"' \
  | head -1 \
  | sed 's/"display_url":"//' \
  | sed 's/"//' \
  | sed 's/\\u0026/\&/g' \
  > temp_url3.txt

if [ -s temp_url3.txt ]; then
    IMAGE_URL3=$(cat temp_url3.txt)
    echo "🔗 URL encontrada: $IMAGE_URL3"
    curl -s "$IMAGE_URL3" -o "data/media/events/evento_3.jpg"
    echo "✅ Evento 3 descargado"
else
    echo "❌ No se pudo obtener la URL del evento 3"
fi

# Limpiar archivos temporales
rm -f temp_url1.txt temp_url2.txt temp_url3.txt

echo "🎉 Proceso completado!"
echo "📁 Imágenes guardadas en: data/media/events/"
