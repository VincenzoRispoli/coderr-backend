# Coderr

Coderr is a platform inspired by Fiverr, designed to **connect clients with freelance developers**.  
Users can register either as **Clients** (looking for services) or as **Freelancers** (offering services through tiered packages).

---

## ✨ Features

- User registration and authentication (Business & Customer roles)
- Custom user profiles with personal information, contact details, and files
- Service offers (gigs) creation and management
- Search and filter functionality for offers
- Order system for purchasing services
- User dashboard for tracking sales and purchases
- RESTful API for frontend and third-party integration

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: SQLite3 for local development
- **Authentication**:Token Authentication
- **Frontend**: HTML/CSS/JavaScript

---

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/VincenzoRispoli/coderr-backend.git

   cd coderr-backend

2. Create and activate virtual enviroment
   ```bash
   python -m venv venv
   
   2.1 Activate the virtual environment (Windows):
   ```bash
   venv\Scripts\activate      # Windows

   2.2 Activate the virtual enviroment (Mac/Linux)
   ```bash
   source venv/bin/activate

   source venv/bin/activate   # Linux/Mac
3. Install dependencies
   ```bash
   pip install -r requirements.txt

4. Apply migrations
   ```bash
   python manage.py migrate

5. Create  superuser
   ```bash
   python manage.py createsuperuser

6. Run the development server
   ```bash
   python manage.py runserver

7. Access the project with ctrl + click over the link at: 
   ```bash
   http://127.0.0.1:8000/


## API-Endpoints

### Registration and Login Endpoints<br>
POST /api/auth/register/ → Register a new user and create a new token<br>
POST /api/auth/login/ → Login and retrieve token

### User Profiles Endpoints<br>
GET /api/profiles/ → List all profiles<br>
GET /api/profiles/{id}/ → Retrieve profile details<br>
PATCH /api/profiles/{id}/ → Update profile (including linked User data)

### Offers Endpoints<br>
GET /api/offers/ → List all available offers<br>
POST /api/offers/ → Create a new offer (business/freelancer only)<br>
GET /api/offers/{id}/ → Retrieve offer details including Basic, Standard, Premium tiers<br>
PATCH /api/offers/{id}/ → Update an offer

### Order Endpoints<br>
GET /api/orders/ → List all availabale orders<br>
GET /api/orders/{id}/ → Retrieve order details<br>
POST /api/orders/ → Create an order for an offer<br>
PATCH /api/orders/ → Update the status of a current order (in progress, completed or stopped)

### Reviews Endpoints<br>
GET /api/reviews/ → List all available reviews<br>
GET /api/reviews/{id}/ → Retrieve review details<br>
POST /api/reviews/ → Create a review for a completed order

### Base Info View**<br>
GET /api/base-info/ → get information about the business profile count, the reviews count, the offers count and the avarage rating

👨‍💻 Contributing

Fork the project

Create your feature branch (git checkout -b feature/feature-name)

Commit your changes (git commit -m "feat: description of feature")

Push to the branch (git push origin feature/feature-name)

Open a Pull Request 🚀
