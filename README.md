# PFA_CarListings: Automated Scraping and Analysis for Car Listings

## Overview
PFA_CarListings is a comprehensive e-commerce solution designed to scrape and analyze car listings from Moroccan platforms like **Avito.ma** and **Moteur.ma**. It integrates automated data collection, real-time data handling, and a Machine Learning-based recommendation system, all wrapped in a user-friendly web application with separate **front-end** and **back-end** components connected via REST APIs.

---

## Repository Structure
- **Backend**: 
  - Built with Django for managing APIs and business logic.
  - Handles web scraping, data storage, and recommendation systems.
- **Frontend**: 
  - Developed with Angular for an interactive and responsive user interface.
  - Displays real-time car listings, filters, and recommendations.
- **Scripts**: 
  - Automates data scraping using tools like Selenium and Beautiful Soup.

---

## How to Run the Project

### Backend Setup
1. **Navigate to the backend directory**:
   ```bash
   cd ~/Bureau/CarListings/Backend
2. **Set up a Python virtual environment**:
    ```bash
    python3 -m venv new_pfa
    source new_pfa/bin/activate

3. **Install necessary dependencies**:
    ```bash
    pip install kafka-python django django-cors-headers djangorestframework
    pip install beautifulsoup4 scikit-learn selenium webdriver-manager panda pandas requests

4. **Run the backend server**:
    ```bash
    python manage.py runserver

### Frontend Setup

1. **Ensure the virtual environment is activated**:
    ```bash
    source new_pfa/bin/activate

2. **nstall Node.js and npm**:
    ```bash
    sudo apt install nodejs npm

3. **Install Angular CLI globally**:
    ```bash
    sudo npm install -g @angular/cli

4. **Navigate to the frontend directory and install dependencies**:
    ```bash
    cd ~/Bureau/CarListings/Frontend/frontend
    npm install zone.js@~0.14.0
    npm install

5. **Start the Angular frontend**:
     ```bash
     ng serve

### Connecting Frontend and Backend

The frontend is pre-configured to connect automatically to the backend through REST APIs. Ensure both the backend and frontend servers are running for full functionality.
After running the command, the frontend will be accessible in your browser at: http://localhost:4200

### Kafka and Zookeeper for Scraping Integration

1. **Start Zookeeper**:
    ```bash    
    bin/zookeeper-server-start.sh config/zookeeper.properties

2. **Start Kafka**:
    ```bash
    bin/kafka-server-start.sh config/server.properties

---

### Features
- **Backend**

    Provides RESTful APIs for managing car listings.
    Features a Machine Learning-powered recommendation system.
    Integrates automated web scraping using Beautiful Soup and Selenium.

- **Frontend**

    Interactive and intuitive interface for browsing and filtering car listings.
    Real-time data visualization and updates.
    Features a car comparison tool and a recommendation engine.

- **Technologies Used**

    Backend: Django, Django REST framework, Kafka, Selenium.
    Frontend: Angular, Zone.js.
    Big Data Integration: Kafka for real-time data handling.
    Web Scraping: Beautiful Soup, Selenium.

---

### Author and Acknowledgments

This project was created by **Aya Laadaili** as part of the Master’s program in **Big Data and Data Science** at Hassan II University of Casablanca.

I would like to express my heartfelt gratitude to:

- **Prof. Marzak Abdelaziz** for his invaluable mentorship and guidance throughout this project.
- The **Hassan II University of Casablanca** for providing support and resources.

---

### Contributions

For any contributions, issues, or suggestions, please feel free to:

- Open an issue on this repository.
- Submit a pull request with your improvements or suggestions.

