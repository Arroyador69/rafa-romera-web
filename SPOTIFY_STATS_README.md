# 🎵 Rafa Romera - Sistema de Estadísticas de Spotify

## 🤖 Sistema de Actualización Automática

Este sistema mantiene las estadísticas de Spotify de Rafa Romera actualizadas automáticamente.

### 📊 Estadísticas Actuales:
- **Oyentes Mensuales**: 28,596
- **Seguidores**: 14,772
- **Fuente**: [Perfil de Spotify de Rafa Romera](https://open.spotify.com/intl-es/artist/5L6WDyrviuO7HkNgMdDeCa)

### 🔄 Cómo Funciona:

#### 1. **GitHub Actions (Automático)**
- ✅ Se ejecuta **diariamente a las 9:00 AM UTC**
- ✅ Scraping automático del perfil de Spotify
- ✅ Actualiza el archivo `data/spotify_stats.json`
- ✅ Hace commit y push automático de los cambios
- ✅ Actualiza el HTML con las nuevas estadísticas

#### 2. **JavaScript (Cliente)**
- ✅ Actualiza las estadísticas cada **5 minutos** en el navegador
- ✅ Carga datos desde `data/spotify_stats.json`
- ✅ Actualización en tiempo real para los usuarios

#### 3. **Scripts Manuales**
- ✅ `python3 update_stats.py` - Actualización manual inmediata
- ✅ `python3 spotify_web_scraper.py` - Scraping avanzado

### 📁 Archivos del Sistema:

```
├── .github/workflows/
│   └── update-spotify-stats.yml    # GitHub Action automático
├── data/
│   └── spotify_stats.json          # Estadísticas en JSON
├── js/
│   └── spotify-stats.js            # Script de actualización en cliente
├── update_stats.py                 # Script manual simple
├── spotify_web_scraper.py          # Scraper avanzado
└── SPOTIFY_STATS_README.md         # Esta documentación
```

### 🚀 Activación del Sistema:

1. **GitHub Action**: Se activa automáticamente al hacer push
2. **Ejecución manual**: Ve a GitHub Actions y ejecuta "Update Spotify Statistics"
3. **Actualización local**: Ejecuta `python3 update_stats.py`

### 📈 Flujo de Actualización:

```
Spotify Profile → GitHub Action → JSON File → HTML Update → Website
     ↓               ↓              ↓           ↓           ↓
  Datos reales → Scraping diario → Almacén → Frontend → Usuarios
```

### ✅ Beneficios:

- 🔄 **Actualización automática** diaria
- 📊 **Datos siempre actualizados** en el sitio web
- 🤖 **Sin intervención manual** necesaria
- 🌐 **Sincronización perfecta** con Spotify
- 📱 **Funciona en todos los dispositivos**

### 🔧 Mantenimiento:

El sistema se mantiene automáticamente. Solo necesitas:
- Verificar que el GitHub Action esté activo
- Revisar ocasionalmente los logs en GitHub Actions
- Actualizar manualmente si es necesario con `python3 update_stats.py`

¡Las estadísticas de Rafa Romera siempre estarán actualizadas! 🎵
