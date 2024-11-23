# mycar/views.py
from itertools import count
import threading
from venv import logger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Car, CarAvito, CarMoteur, Admin, Client, Sauvegarde, Visite 
from .serializers import AdminSerializer, CarAvitoSerializer, CarMoteurSerializer, ClientSerializer, User, UserSerializer
from appcar.scrapers.kafka_producer import scrape_moteur_data, scrape_avito_data
from appcar.scrapers.kafka_consumer import store_in_database , start_consumer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .services.recommendations import recommend_cars
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
@api_view(['GET'])
def get_recommendations(request, user_id):
    recommendations = recommend_cars(user_id)
    return JsonResponse(recommendations.to_dict(orient='records'), safe=False)
def index(request):
    return render(request, 'index.html')

def scrape_moteur(request):
    scrape_moteur_data()

    # Return an immediate response
    return HttpResponse("Scraping Moteur started, consumer running in background.")

def scrape_avito(request):
    scrape_avito_data()
    
    
    # Return an immediate response
    return HttpResponse("Scraping Avito started, consumer running in background.")


class CarDataView(APIView):
    def get(self, request, *args, **kwargs):
        avito_cars = CarAvito.objects.all()

        avito_serializer = CarAvitoSerializer(avito_cars, many=True)

        data = {
            'avito_cars': avito_serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
@api_view(['POST'])
def logIn(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if Client.objects.filter(user=user).exists():
                response = JsonResponse({'redirectUrl': f'/dashboard_client/{user.id}/'})
            elif Admin.objects.filter(user=user).exists():
                response = JsonResponse({'redirectUrl': f'/dashboard_admin/{user.id}/'})
            else:
                response = JsonResponse({'redirectUrl': '/login'})
            response["Access-Control-Allow-Origin"] = "*"
            return response
        else:
            return JsonResponse({'error': 'Mauvaise authentification'}, status=401)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['POST'])
def logOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Vous avez été bien déconnecté')
        return redirect('login')

class AdminSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser] 

    def create(self, request, *args, **kwargs):
        data = request.data
        user_data = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': data.get('password'),
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            admin_data = {
                'user': user.id,
                'role': 'admin'
            }
            admin_serializer = AdminSerializer(data=admin_data)
            if admin_serializer.is_valid():
                admin_serializer.save()
                return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminListView(APIView):
    def get(self, request, *args, **kwargs):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClientSignupView(APIView):
    def post(self, request, *args, **kwargs):
        print("Données reçues:", request.data) 
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Erreurs de validation:", serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientListView(APIView):
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')

def admin_dashboard_view(request):
    return Response({'message': 'Admin dashboard'})

def client_dashboard_view(request, client_id):
    return Response({'message': f'Client dashboard for client ID: {client_id}'})


@require_GET
def record_visit(request, user_id, car_id):
    try:
        # Récupérer l'utilisateur par ID
        user = User.objects.get(id=user_id)
        # Récupérer le client associé à cet utilisateur
        client = Client.objects.get(user=user)
        try:
            car = CarAvito.objects.get(id_car=car_id)
        except CarAvito.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Car not found'}, status=404)

        Visite.objects.create(client=client, car=car)
        return JsonResponse({'status': 'success'})
    except Client.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Client not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
   
@require_GET
def record_save(request, user_id, car_id):
    try:
        # Récupérer l'utilisateur par ID
        user = User.objects.get(id=user_id)
        # Récupérer le client associé à cet utilisateur
        client = Client.objects.get(user=user)
        try:
            car = CarAvito.objects.get(id_car=car_id)
        except CarAvito.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Car not found'}, status=404)

        # Enregistrement dans Sauvegarde
        Sauvegarde.objects.get_or_create(client=client, car=car)
        return JsonResponse({'status': 'success'})
    except Client.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Client not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    
def car_details(request, id):
    car = get_object_or_404(CarAvito.objects.all(), id_car=id)
    
    data = {
        'id_car': car.id_car,
        'title': car.title,
        'price': car.price,
        'carburant': car.carburant,
        'boite': car.boite,
        'kilometrage': car.kilometrage,
        'year': car.year,
        'ville': car.ville,
        'nombre_de_portes': getattr(car, 'nombre_de_portes', None),
        'autor': getattr(car, 'autor', None),
        'etat': getattr(car, 'etat', None)
    }
    return JsonResponse(data)

def get_car_count(request):
    total_avito_cars = CarAvito.objects.count()
    total_moteur_cars = CarMoteur.objects.count()
    total_cars = total_avito_cars + total_moteur_cars
    return JsonResponse({'count': total_cars})

def get_client_count(request):
    total_clients = Client.objects.count()
    return JsonResponse({'count': total_clients})

@api_view(['GET'])
def get_saved_cars(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)
    saved_cars = Sauvegarde.objects.filter(client=client).select_related('car')
    car_data = []

    for saved_car in saved_cars:
        car = saved_car.car
        car_data.append({
            'id_car': car.id_car,
            'title': car.title,
            'price': car.price,
            'carburant': car.carburant,
            'boite': car.boite,
            'puissance_fiscale': car.puissance_fiscale,
            'image_url': car.image_url,
            'url': car.url,
            'kilometrage': car.kilometrage,
            'year': car.year,
            'ville': car.ville,
            'scraped_at': car.scraped_at,
            'nombre_de_portes': car.nombre_de_portes,
            'autor': car.autor,
            'etat': car.etat,
        })

    return JsonResponse(car_data, safe=False)

