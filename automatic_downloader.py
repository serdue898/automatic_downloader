from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
from tqdm import tqdm

# Configura Selenium con el controlador de Firefox
driver = None
try:
    driver = webdriver.Firefox()
except Exception as e:
    print(f"Error al iniciar WebDriver: {e}")
    exit(1)

print("ingrese el enlace de la carpeta de mediafire")
folder_url = input()

# Carpeta local donde se guardarán los archivos descargados
output_folder = "C:/Users/ADMIN/Downloads/mafia"
os.makedirs(output_folder, exist_ok=True)

def get_file_links(folder_url):
    """
    Función para obtener los enlaces de descarga directa de una carpeta de Mediafire usando Selenium
    """
    driver.get(folder_url)
    time.sleep(5)  # Espera a que la página cargue completamente
    
    # Encuentra todos los enlaces dentro de la carpeta
    links = driver.find_elements(By.TAG_NAME, "a")
    
    download_links = []
    for link in links:
        href = link.get_attribute('href')
        if href and 'mediafire.com/file/' in href:
            if not href in download_links:
                download_links.append(href)
    
    return download_links

def download_file(url, folder):
    """
    Función para descargar un archivo dado su URL y guardarlo en una carpeta
    """
    print(f"Descargando {url}...")
    
    while True:
        try:
            driver.set_page_load_timeout(10)
            driver.get(url)
            link = WebDriverWait(driver, 0.5,0.1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.input.popsok"))
            )
            
            download_url = link.get_attribute('href')
            
            response = requests.get(download_url, allow_redirects=True, stream=True)
            # Extrae el nombre del archivo
            filename = os.path.join(folder, url.split('/')[5])
            
            total_size = int(response.headers.get('content-length', 0))
            break
        except Exception as e:
            print(f"Error al obtener el enlace de descarga: {e}")
        
    
    # Descarga el archivo y muestra el progreso
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
    
    print(f"{filename} descargado con éxito.")

# Obtener los enlaces de los archivos en la carpeta de Mediafire
file_links = get_file_links(folder_url)

# Descargar cada archivo
for link in file_links:
    download_file(link, output_folder)

# Cierra el navegador
if driver:
    driver.quit()
