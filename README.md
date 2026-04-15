# Rural2Urban

## Overview

Rural2Urban is a full-stack e-commerce platform designed to connect rural producers with urban consumers. The system enables customers to browse products, place orders, and pay via M-Pesa, while vendors manage inventory and fulfill orders through an integrated dashboard.

---

## Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* Zustand (state management)
* Axios (API communication)

### Backend

* Django REST Framework
* PostgreSQL
* JWT Authentication (SimpleJWT)

### Integrations

* M-Pesa Daraja API (payments)
* WebSockets (real-time features - optional)

---

## Project Structure

```bash
rural2urban/
├── backend/              # Django backend (API, business logic)
├── frontend/             # React frontend (UI, client-side logic)
├── README.md
```

---

## Backend Architecture (Django)

```bash
backend/
├── config/               # Project settings & configuration
│   ├── settings.py
│   ├── urls.py
│
├── apps/                 # Domain-based apps
│   ├── users/
│   ├── products/
│   ├── orders/
│   ├── payments/
│   └── reviews/
│
├── common/               # Shared logic
│   ├── utils.py
│   ├── permissions.py
│   ├── exceptions.py
│   └── responses.py
```

### Backend Principles

* Each app represents a business domain
* Views handle request/response logic
* Serializers handle validation and transformation
* Models define database structure
* Optional service layer for complex business logic

---

## Frontend Architecture (React)

```bash
frontend/
├── src/
│   ├── app/                  # App setup (routes, providers)
│   ├── features/             # Domain-based features
│   │   ├── auth/
│   │   ├── products/
│   │   ├── orders/
│   │   ├── payments/
│   │   └── vendor/
│   │
│   ├── shared/               # Reusable logic
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── services/
│   │
│   ├── styles/
│   └── main.jsx
```

### Frontend Principles

* Feature-based architecture
* Each feature owns its state, API, and components
* Shared folder contains reusable logic
* Pages are thin and focused on routing

---

## Core Features

### Customer (Buyer)

* Register / Login
* Browse and search products
* Filter products by category or price
* Add to cart and manage cart
* Place orders
* Pay via M-Pesa (STK push)
* Track order status
* Leave reviews

---

### Vendor (Shop Owner)

* Manage products (add/edit/delete)
* Manage stock levels
* View incoming orders
* Update order status
* View sales reports

---

### Rider (Optional / Future)

* Register and get approved
* Accept delivery jobs
* Mark deliveries as completed
* View earnings

---

### Admin

* Manage users (buyers, vendors, riders)
* Monitor orders and transactions
* Handle disputes
* View analytics
* Manage categories

---

## Authentication Flow

1. User registers or logs in
2. Backend returns JWT tokens (access + refresh)
3. Tokens stored in frontend (localStorage or secure storage)
4. Requests include Authorization header:

   ```
   Bearer <access_token>
   ```
5. Token refresh handled automatically when expired

---

## Payment Flow (M-Pesa)

1. User enters phone number at checkout
2. STK push sent to user's phone
3. User enters M-Pesa PIN
4. Daraja API confirms payment
5. Backend updates order status → paid
6. User and vendor are notified

---

## Development Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd rural2urban
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create `.env` files for both frontend and backend.

### Backend (.env)

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_postgres_url
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000/api/
```

---

## Deployment

### Frontend

* Deploy using Vercel

### Backend

* Deploy using Render or Railway

### Database

* PostgreSQL (cloud)

### Domain

* Connect custom domain (e.g. rural2urban.co.ke)

---

## Coding Principles

* Write code you understand
* Build one feature at a time
* Test backend before frontend integration
* Keep components small and reusable
* Avoid unnecessary complexity early

---

## Future Improvements

* Real-time order tracking
* Advanced analytics dashboard
* AI-powered assistant
* Multi-language support
* Mobile app version

---

## Author

* Benson Ragira

---
