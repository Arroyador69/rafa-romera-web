# Web para Rafa Romera

Este proyecto contiene un script de web scraping para recopilar información pública sobre el cantante Rafa Romera, con el objetivo de crear su página web oficial.

## 🚀 Características

- Extracción de biografía de Wikipedia
- Recopilación de enlaces a redes sociales
- Estructura organizada de datos en carpetas
- Soporte para sitios dinámicos con Selenium

## 📋 Requisitos

- Python 3.8 o superior
- Chrome/Chromium instalado (para Selenium)
- Dependencias listadas en `requirements.txt`

## 🔧 Instalación

1. Clona este repositorio
2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

Para ejecutar el scraper:

```bash
python scraper.py
```

Los datos se guardarán en la carpeta `data/` con la siguiente estructura:
- `bio/`: Biografía y trayectoria
- `music/`: Información sobre discografía
- `media/`: Fotos y portadas
- `events/`: Próximos conciertos y eventos
- `social/`: Enlaces a redes sociales
- `videos/`: Entrevistas y videoclips

## 📝 Notas

- El script está diseñado para extraer información pública disponible
- Se recomienda revisar los términos de servicio de cada plataforma antes de usar el scraper
- Los datos extraídos deben ser utilizados respetando los derechos de autor

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos. 
