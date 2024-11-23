import random
import time
from kafka import KafkaProducer
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Wait for acknowledgment from the consumer
)

def produce_car_data(car_data):
    producer.send('car_listings', value=car_data).get(timeout=60)  # Send and wait for acknowledgment
    logger.info(f"Produced car data: {car_data['title']}")

def get_additional_data(listing_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(listing_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {listing_url}: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    
    details = {
        'etat': 'N/A',
        'annee': 'N/A',
        'kilometrage': 'N/A',
        'ville': 'N/A'
    }

    # Extract additional details
    detail_items = soup.select('div.sc-qmn92k-0.cjptpz li.sc-qmn92k-1.jJjeGO')
    for item in detail_items:
        label = item.select_one('span.sc-1x0vz2r-0.jZyObG')
        value = item.select_one('span.sc-1x0vz2r-0.gSLYtF')
        if label and value:
            label_text = label.get_text(strip=True)
            value_text = value.get_text(strip=True)
            if 'État' in label_text:
                details['etat'] = value_text
            elif 'Année-Modèle' in label_text:
                details['annee'] = value_text
            elif 'Kilométrage' in label_text:
                details['kilometrage'] = value_text

    ville_element = soup.select_one('div.sc-1g3sn3w-7.bNWHpB span.sc-1x0vz2r-0.iotEHk')
    if ville_element:
        details['ville'] = ville_element.get_text(strip=True)

    return details

def scrape_avito_data():
    url_avito = "https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre"
    container_anchors_class = "sc-1jge648-0 eTbzNs"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(60)

        for i in range(1, 130):  # Adjust the range based on how many pages you want to scrape
            url_page = f"{url_avito}?o={i}" if i != 1 else url_avito
            logger.info(f"Scraping page {i} from {url_avito}")
            driver.get(url_page)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, container_anchors_class.split()[0])))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            container_anchors = soup.find_all('a', class_=container_anchors_class)

            for container_anchor in container_anchors:
                try:
                    title_element = container_anchor.find('p', class_="sc-1x0vz2r-0 czqClV")
                    price_element = container_anchor.find('p', class_="sc-1x0vz2r-0 eCXWei sc-b57yxx-3 IneBF")
                    autor_element = container_anchor.find('p', class_="sc-1x0vz2r-0 dNKvDA")
                    carburant_element = container_anchor.find('div', title="Type de carburant")
                    boite_element = container_anchor.find('div', title="Boite de vitesses")
                    puissance_fiscale_element = container_anchor.find('div', title="Puissance fiscale")
                    image_element = container_anchor.find('img', class_="sc-bsm2tm-3 krcAcS")
                    url_suffix = container_anchor['href']

                    if not url_suffix:
                        logger.warning("URL is null or empty, skipping.")
                        continue

                    full_url = f"https://www.avito.ma{url_suffix}" if url_suffix.startswith('/') else url_suffix

                    title = title_element.text.strip() if title_element else 'N/A'
                    price = price_element.text.strip() if price_element else 'N/A'
                    autor = autor_element.text.strip() if autor_element else 'N/A'
                    carburant = carburant_element.span.text.strip() if carburant_element and carburant_element.span else 'N/A'
                    boite = boite_element.span.text.strip() if boite_element and boite_element.span else 'N/A'
                    puissance_fiscale = puissance_fiscale_element.span.text.strip() if puissance_fiscale_element and puissance_fiscale_element.span else 'N/A'
                    image_url = image_element['src'] if image_element else 'N/A'

                    additional_data = get_additional_data(full_url)

                    car_data = {
                        'title': title,
                        'price': price,
                        'autor': autor,
                        'carburant': carburant,
                        'boite': boite,
                        'puissance_fiscale': puissance_fiscale,
                        'image_url': image_url,
                        'etat': additional_data.get('etat', 'N/A'),
                        'year': additional_data.get('annee', 'N/A'),
                        'kilometrage': additional_data.get('kilometrage', 'N/A'),
                        'ville': additional_data.get('ville', 'N/A'),
                        'url': full_url,
                        'source': 'avito'
                    }
                    
                    # Send data to Kafka immediately after scraping
                    produce_car_data(car_data)

                except Exception as e:
                    logger.error(f"Error parsing container anchor: {e}")
                    continue

    except Exception as e:
        logger.error(f"Error scraping Avito: {e}")
    finally:
        driver.quit()

    logger.info("Scraping Avito data completed.")

def get_page_url(base_url, page_number):
    return f"{base_url}?page={page_number}"

def get_listing_urls(page_url):
    """Fetch listing URLs from the specified Moteur page URL."""
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listing_anchors = soup.find_all('a', class_='listing-link')  # Adjust the class as needed
        return [anchor['href'] for anchor in listing_anchors if 'href' in anchor.attrs]
    except Exception as e:
        logger.error(f"Error fetching listing URLs from {page_url}: {e}")
        return []

def get_car_data(car_url):
    """Fetch car data from the specific listing page."""
    try:
        response = requests.get(car_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse necessary data from the car listing page (example selectors)
        title = soup.select_one('h1.car-title').get_text(strip=True) if soup.select_one('h1.car-title') else 'N/A'
        price = soup.select_one('.price').get_text(strip=True) if soup.select_one('.price') else 'N/A'
        year = soup.select_one('.year').get_text(strip=True) if soup.select_one('.year') else 'N/A'
        ville = soup.select_one('.location').get_text(strip=True) if soup.select_one('.location') else 'N/A'
        carburant = soup.select_one('.carburant').get_text(strip=True) if soup.select_one('.carburant') else 'N/A'
        image_url = soup.select_one('.car-image')['src'] if soup.select_one('.car-image') else 'N/A'
        kilometrage = soup.select_one('.kilometrage').get_text(strip=True) if soup.select_one('.kilometrage') else 'N/A'
        boite = soup.select_one('.boite').get_text(strip=True) if soup.select_one('.boite') else 'N/A'
        puissance_fiscale = soup.select_one('.puissance-fiscale').get_text(strip=True) if soup.select_one('.puissance-fiscale') else 'N/A'

        return {
            'url': car_url,
            'title': title,
            'price': price,
            'year': year,
            'ville': ville,
            'carburant': carburant,
            'kilometrage': kilometrage,
            'boite': boite,
            'puissance_fiscale': puissance_fiscale,
            'image_url': image_url,
            'source': 'moteur'
        }
    except Exception as e:
        logger.error(f"Error fetching car data from {car_url}: {e}")
        return None
def scrape_moteur_data():
    base_url_moteur = "https://www.moteur.ma/voitures-a-vendre"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(60)

        for i in range(1, 130):  # Adjust based on how many pages you want to scrape
            page_url = f"{base_url_moteur}?page={i}"
            logger.info(f"Scraping page {i} from {base_url_moteur}")
            driver.get(page_url)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-link')))
            time.sleep(random.uniform(2, 5))

            listing_urls = [anchor['href'] for anchor in BeautifulSoup(driver.page_source, "html.parser").find_all('a', class_='listing-link') if 'href' in anchor.attrs]

            for listing_url in listing_urls:
                try:
                    car_data = get_car_data(listing_url)
                    if car_data:
                        produce_car_data(car_data)
                        logger.info(f"Produced car data: {car_data['title']} from Moteur")
                except Exception as e:
                    logger.error(f"Error processing listing URL {listing_url}: {e}")
                    continue

    except Exception as e:
        logger.error(f"Error scraping Moteur: {e}")
    finally:
        driver.quit()

    logger.info("Scraping Moteur data completed.")

if __name__ == "__main__":
    while True:
        scrape_avito_data()
        scrape_moteur_data()
        time.sleep(random.uniform(60, 120))