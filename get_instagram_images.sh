#!/bin/bash

# Crear directorio si no existe
mkdir -p data/media/events

echo "🎬 Descargando imágenes de Instagram con método alternativo..."

# Función para descargar imagen de Instagram
download_instagram_image() {
    local url=$1
    local filename=$2
    local event_num=$3
    
    echo "📥 Descargando evento $event_num..."
    
    # Intentar múltiples métodos para obtener la imagen
    # Método 1: Buscar display_url
    IMAGE_URL=$(curl -s "$url" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
        -H "Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3" \
        -H "Accept-Encoding: gzip, deflate, br" \
        -H "DNT: 1" \
        -H "Connection: keep-alive" \
        -H "Upgrade-Insecure-Requests: 1" \
        | grep -o '"display_url":"[^"]*"' \
        | head -1 \
        | sed 's/"display_url":"//' \
        | sed 's/"//' \
        | sed 's/\\u0026/\&/g')
    
    # Si no funciona, intentar con thumbnail_src
    if [ -z "$IMAGE_URL" ]; then
        IMAGE_URL=$(curl -s "$url" \
            -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
            | grep -o '"thumbnail_src":"[^"]*"' \
            | head -1 \
            | sed 's/"thumbnail_src":"//' \
            | sed 's/"//' \
            | sed 's/\\u0026/\&/g')
    fi
    
    # Si aún no funciona, intentar con og:image
    if [ -z "$IMAGE_URL" ]; then
        IMAGE_URL=$(curl -s "$url" \
            -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
            | grep -o '<meta property="og:image" content="[^"]*"' \
            | sed 's/<meta property="og:image" content="//' \
            | sed 's/"//')
    fi
    
    if [ -n "$IMAGE_URL" ]; then
        echo "🔗 URL encontrada: $IMAGE_URL"
        curl -s "$IMAGE_URL" -o "$filename"
        if [ -s "$filename" ]; then
            echo "✅ Evento $event_num descargado exitosamente"
            return 0
        else
            echo "❌ Error descargando imagen del evento $event_num"
            return 1
        fi
    else
        echo "❌ No se pudo obtener la URL del evento $event_num"
        return 1
    fi
}

# Descargar las tres imágenes
download_instagram_image "https://www.instagram.com/p/DOjJbPJjPUH/?hl=es" "data/media/events/evento_1.jpg" 1
download_instagram_image "https://www.instagram.com/p/DO5nx9MjAfD/?hl=es" "data/media/events/evento_2.jpg" 2
download_instagram_image "https://www.instagram.com/p/DOYc5__jBGZ/?hl=es" "data/media/events/evento_3.jpg" 3

echo "🎉 Proceso completado!"
echo "📁 Verificando archivos descargados..."

# Verificar qué archivos se descargaron
ls -la data/media/events/
