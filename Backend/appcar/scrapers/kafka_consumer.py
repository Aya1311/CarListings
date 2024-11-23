import threading
import json
import logging
from kafka import KafkaConsumer
from django.http import HttpResponse
from mycar.models import CarAvito, CarMoteur
from django.utils.timezone import now
from django.db import transaction
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_consumer():
    """Function to start the Kafka consumer and process messages."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycar.settings')  
    import django
    django.setup()

    consumer = KafkaConsumer(
        'car_listings',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='car_group',
        auto_offset_reset='earliest'
    )

    logger.info("Kafka consumer started...")
    try:
        for message in consumer:
            car_data = message.value
            logger.info(f"Consumed message: {car_data}")
            store_in_database(car_data)
    except Exception as e:
        logger.error(f"Error in consumer: {e}")
    finally:
        consumer.close()

def store_in_database(car_data):
    """Store car data in the database based on its source."""
    try:
        with transaction.atomic():  
            if car_data['source'] == 'avito':
                car = CarAvito(
                    title=car_data['title'],
                    price=car_data['price'],
                    autor=car_data.get('autor', "N/A"),
                    carburant=car_data.get('carburant', None),
                    boite=car_data.get('boite', None),
                    puissance_fiscale=car_data.get('puissance_fiscale', None),
                    image_url=car_data.get('image_url', None),
                    etat=car_data.get('etat', "N/A"),
                    year=car_data.get('year', None),
                    kilometrage=car_data.get('kilometrage', None),
                    ville=car_data.get('ville', None),
                    url=car_data['url'],
                    scraped_at=now()
                )
                car.save()
            elif car_data['source'] == 'moteur':
                car = CarMoteur(
                    title=car_data['title'],
                    price=car_data['price'],
                    autor=car_data.get('autor', "N/A"),
                    carburant=car_data.get('carburant', None),
                    boite=car_data.get('boite', None),
                    puissance_fiscale=car_data.get('puissance_fiscale', None),
                    image_url=car_data.get('image_url', None),
                    etat=car_data.get('etat', "N/A"),
                    year=car_data.get('year', None),
                    kilometrage=car_data.get('kilometrage', None),
                    ville=car_data.get('ville', None),
                    url=car_data['url'],
                    scraped_at=now()
                )
                car.save()
            logger.info(f"Successfully stored car data: {car_data['title']} in the database.")
    except Exception as e:
        logger.error(f"Failed to store car data: {e}. Data: {car_data}")

def consume_messages(request):
    """Start the Kafka consumer in a separate thread."""
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    
    # Return an immediate response
    return HttpResponse("Consumer started, running in the background.")
