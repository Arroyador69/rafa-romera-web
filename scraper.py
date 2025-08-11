import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import shutil
from urllib.parse import urlparse
from logging_config import setup_logging

class RafaRomeraScraper:
    def __init__(self):
        self.base_dir = "data"
        self.logger = setup_logging(self.base_dir)
        self.create_directories()
        self.setup_selenium()

    def create_directories(self):
        """Crea la estructura de directorios para almacenar los datos"""
        try:
            directories = [
                "bio",
                "music",
                "media",
                "events",
                "social",
                "videos",
                "logs"
            ]
            
            for directory in directories:
                path = os.path.join(self.base_dir, directory)
                os.makedirs(path, exist_ok=True)
                self.logger.info(f"Directorio creado/verificado: {path}")
                
        except Exception as e:
            self.logger.error(f"Error al crear directorios: {str(e)}")
            raise

    def setup_selenium(self):
        """Configura el driver de Selenium para sitios dinámicos"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Driver de Selenium configurado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error al configurar Selenium: {str(e)}")
            raise

    def safe_get_element(self, by, value, timeout=10):
        """Intenta obtener un elemento de forma segura con manejo de errores"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Timeout al buscar elemento: {value}")
            return None
        except NoSuchElementException:
            self.logger.warning(f"Elemento no encontrado: {value}")
            return None
        except Exception as e:
            self.logger.error(f"Error al buscar elemento {value}: {str(e)}")
            return None

    def scrape_biography(self):
        """Extrae la biografía de Wikipedia"""
        try:
            self.logger.info("Iniciando extracción de biografía")
            url = "https://es.wikipedia.org/wiki/Rafa_Romera"
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', {'class': 'mw-parser-output'})
            
            if content:
                paragraphs = content.find_all('p')
                bio_text = '\n'.join([p.get_text() for p in paragraphs[:3]])
                
                bio_file = os.path.join(self.base_dir, 'bio', 'biography.txt')
                with open(bio_file, 'w', encoding='utf-8') as f:
                    f.write(bio_text)
                
                self.logger.info(f"Biografía guardada en {bio_file}")
            else:
                self.logger.warning("No se encontró contenido de biografía")
                
        except requests.RequestException as e:
            self.logger.error(f"Error de conexión al obtener biografía: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error inesperado al extraer biografía: {str(e)}")

    def scrape_discography(self):
        """Extrae información de discografía desde Spotify"""
        try:
            self.logger.info("Iniciando extracción de discografía")
            self.driver.get("https://open.spotify.com/artist/rafaromera")
            time.sleep(5)
            
            albums = []
            singles = []
            
            album_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="album"]')
            single_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="single"]')
            
            for album in album_elements:
                try:
                    title = album.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text
                    year = album.find_element(By.CSS_SELECTOR, '[data-testid="year"]').text
                    albums.append({"title": title, "year": year})
                    self.logger.debug(f"Álbum encontrado: {title} ({year})")
                except NoSuchElementException:
                    continue
            
            for single in single_elements:
                try:
                    title = single.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text
                    year = single.find_element(By.CSS_SELECTOR, '[data-testid="year"]').text
                    singles.append({"title": title, "year": year})
                    self.logger.debug(f"Single encontrado: {title} ({year})")
                except NoSuchElementException:
                    continue
            
            discography = {
                "albums": albums,
                "singles": singles
            }
            
            discography_file = os.path.join(self.base_dir, 'music', 'discography.json')
            with open(discography_file, 'w', encoding='utf-8') as f:
                json.dump(discography, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Discografía guardada en {discography_file}")
            
        except WebDriverException as e:
            self.logger.error(f"Error de Selenium al extraer discografía: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error inesperado al extraer discografía: {str(e)}")

    def scrape_events(self):
        """Extrae información de eventos y conciertos"""
        try:
            # Buscar en Wegow
            self.driver.get("https://www.wegow.com/es/artists/rafa-romera")
            time.sleep(5)
            
            events = []
            event_elements = self.driver.find_elements(By.CSS_SELECTOR, '.event-card')
            
            for event in event_elements:
                try:
                    date = event.find_element(By.CSS_SELECTOR, '.date').text
                    venue = event.find_element(By.CSS_SELECTOR, '.venue').text
                    location = event.find_element(By.CSS_SELECTOR, '.location').text
                    link = event.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    
                    events.append({
                        "date": date,
                        "venue": venue,
                        "location": location,
                        "link": link
                    })
                except:
                    continue
            
            with open(os.path.join(self.base_dir, 'events', 'upcoming_events.json'), 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=4, ensure_ascii=False)
            
            print("✅ Eventos extraídos y guardados correctamente")
            
        except Exception as e:
            print(f"❌ Error al extraer eventos: {str(e)}")

    def scrape_social_media(self):
        """Extrae información de redes sociales"""
        social_data = {
            "instagram": "https://www.instagram.com/rafaromera/",
            "youtube": "https://www.youtube.com/@RafaRomera",
            "spotify": "https://open.spotify.com/artist/rafaromera"
        }
        
        try:
            # Guardar enlaces de redes sociales
            with open(os.path.join(self.base_dir, 'social', 'social_media.json'), 'w', encoding='utf-8') as f:
                json.dump(social_data, f, indent=4, ensure_ascii=False)
            
            print("✅ Enlaces de redes sociales guardados correctamente")
        except Exception as e:
            print(f"❌ Error al guardar enlaces de redes sociales: {str(e)}")

    def download_image(self, url, filename):
        """Descarga una imagen desde una URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            
            self.logger.debug(f"Imagen descargada: {filename}")
            return True
            
        except requests.RequestException as e:
            self.logger.error(f"Error al descargar imagen {url}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error inesperado al descargar imagen {url}: {str(e)}")
        return False

    def scrape_photos(self):
        """Extrae fotos de Instagram"""
        try:
            self.driver.get("https://www.instagram.com/rafaromera/")
            time.sleep(5)
            
            # Esperar a que carguen las imágenes
            photos = self.driver.find_elements(By.CSS_SELECTOR, 'article img')
            
            # Crear directorio para fotos si no existe
            photos_dir = os.path.join(self.base_dir, 'media', 'photos')
            os.makedirs(photos_dir, exist_ok=True)
            
            # Descargar las primeras 10 fotos
            for i, photo in enumerate(photos[:10]):
                try:
                    img_url = photo.get_attribute('src')
                    if img_url:
                        filename = os.path.join(photos_dir, f'photo_{i+1}.jpg')
                        if self.download_image(img_url, filename):
                            print(f"✅ Foto {i+1} descargada correctamente")
                except:
                    continue
            
            print("✅ Fotos extraídas correctamente")
            
        except Exception as e:
            print(f"❌ Error al extraer fotos: {str(e)}")

    def scrape_videos(self):
        """Extrae videos de YouTube"""
        try:
            self.driver.get("https://www.youtube.com/@RafaRomera/videos")
            time.sleep(5)
            
            videos = []
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer')
            
            for video in video_elements[:5]:  # Limitar a los 5 videos más recientes
                try:
                    title = video.find_element(By.CSS_SELECTOR, '#video-title').text
                    link = video.find_element(By.CSS_SELECTOR, '#video-title').get_attribute('href')
                    thumbnail = video.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    
                    videos.append({
                        "title": title,
                        "link": link,
                        "thumbnail": thumbnail
                    })
                except:
                    continue
            
            # Guardar información de videos
            with open(os.path.join(self.base_dir, 'videos', 'videos.json'), 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=4, ensure_ascii=False)
            
            # Descargar miniaturas
            thumbnails_dir = os.path.join(self.base_dir, 'media', 'thumbnails')
            os.makedirs(thumbnails_dir, exist_ok=True)
            
            for i, video in enumerate(videos):
                if video['thumbnail']:
                    filename = os.path.join(thumbnails_dir, f'thumbnail_{i+1}.jpg')
                    if self.download_image(video['thumbnail'], filename):
                        print(f"✅ Miniatura {i+1} descargada correctamente")
            
            print("✅ Videos extraídos correctamente")
            
        except Exception as e:
            print(f"❌ Error al extraer videos: {str(e)}")

    def close(self):
        """Cierra el driver de Selenium"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                self.logger.info("Driver de Selenium cerrado correctamente")
        except Exception as e:
            self.logger.error(f"Error al cerrar el driver: {str(e)}")

def main():
    scraper = None
    try:
        scraper = RafaRomeraScraper()
        scraper.logger.info("🚀 Iniciando scraping de información de Rafa Romera...")
        
        scraper.scrape_biography()
        scraper.scrape_discography()
        scraper.scrape_events()
        scraper.scrape_social_media()
        scraper.scrape_photos()
        scraper.scrape_videos()
        
        scraper.logger.info("✨ Proceso de scraping completado")
    except Exception as e:
        if scraper:
            scraper.logger.error(f"Error fatal durante el scraping: {str(e)}")
        else:
            print(f"Error fatal durante la inicialización: {str(e)}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main() 