PFA_CarListings: Automated Scraping and Analysis for Car Listings
Overview

This project is designed to scrape and analyze car listings from Moroccan platforms Avito.ma and Moteur.ma, creating an all-in-one e-commerce solution for used vehicles. It features a web application with separate front-end and back-end components connected via REST APIs.
Repository Structure

    Backend: Django-based backend for data handling and API management.
    Frontend: Angular-based frontend for user interaction.
    Scripts: Web scraping scripts to automate data collection.

How to Run the Project
Setup Backend

    Navigate to the backend directory:

cd ~/Bureau/PFA_V3_F/appcar_V7

Set up the Python virtual environment:

python3 -m venv new_pfa
source new_pfa/bin/activate

Install dependencies:

pip install kafka-python
pip install django
pip install django-cors-headers
pip install djangorestframework
pip install beautifulsoup4
pip install scikit-learn
pip install selenium
pip install webdriver-manager
pip install panda
pip install pandas
pip install requests

Run the backend server:

    python manage.py runserver

Setup Frontend

    Activate the virtual environment if not already active:

source new_pfa/bin/activate

Install Node.js and npm:

sudo apt install nodejs npm

Install Angular CLI globally:

sudo npm install -g @angular/cli

Navigate to the frontend directory and install dependencies:

cd ~/Bureau/PFA_V3_F/appcar_V7/frontend
npm install zone.js@~0.14.0
npm install

Start the Angular frontend:

    ng serve

Connecting Frontend and Backend

    The frontend is configured to automatically connect to the backend via REST APIs. Ensure both servers are running.

Kafka and Zookeeper (Optional for Scraping Integration)

    Start Zookeeper:

bin/zookeeper-server-start.sh config/zookeeper.properties

Start Kafka:

    bin/kafka-server-start.sh config/server.properties

Features

    Backend:
        RESTful APIs for managing car listings.
        Machine Learning-based recommendation system.
        Automated web scraping using Selenium and Beautiful Soup.

    Frontend:
        User-friendly interface for browsing and comparing cars.
        Real-time updates using Angular.
        Integrated search and filtering options.

Technologies Used

    Backend: Django, REST framework, Kafka, Selenium.
    Frontend: Angular, Zone.js.
    Big Data: Kafka for real-time data handling.
    Web Scraping: Beautiful Soup, Selenium.

Acknowledgments

Special thanks to:

    Prof. Marzak Abdelaziz for mentorship and guidance.
    The Hassan II University community for their support.

For any contributions or issues, please raise them in this repository.
