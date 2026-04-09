# Crop Recommendation System
**Crop Recommendation System** predicts the most suitable crop to grow based on key soil and environmental factors such as:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH value
- Rainfall

The system uses a trained Random Forest Machine Learning model integrated into a Django web application.

---


## Features

### Multi-User Roles
- **Public Users** → View general information  
- **Logged-in Users** → Get personalized crop predictions  
- **Admin Panel** →  
  - Manage users   
  - Analyze total users  
  - View user predictions  
  - Identify most recommended crops

--- 

### Machine Learning Integration
- Model Used: **Random Forest Classifier**
- Accuracy: **99.39%**
- Accepts:
  - Manual input values
  - Random sample upload option
- Output:
  - Recommended crop name  
  - Input feature values summary  

---

### Web Application
- Built using **Django Framework**
- Clean and responsive UI using:
  - Bootstrap 5  
  - SweetAlert2  

---

### Database Management
- Development: SQLite  
- Production: PostgreSQL  
- Managed using Django ORM  

---

### Authentication System
- Django’s built-in authentication system  
- Secure login & user management  

---

## Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, Bootstrap 5, CSS  
- **Machine Learning:** Scikit-learn (Random Forest)  
- **Database:** SQLite (Dev), PostgreSQL (Production)  
- **Deployment:** Vercel  

---

## Model Performance

- Algorithm: Random Forest  
- Accuracy: **0.9939 (~99.39%)**

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/crop-recommendation.git
cd crop-recommendation
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/crop-recommendation.git
cd crop-recommendation
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory and add required variables (e.g., SECRET_KEY, DB config).

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Run the Server
```bash
python manage.py runserver
```

## Live Demo

👉 **Live Project:** [https://crop-recommendation-zeta.vercel.app/]

---

## Dataset

- Source: Kaggle  
- Features used:
  - N, P, K  
  - Temperature  
  - Humidity  
  - pH  
  - Rainfall  

---

## How It Works

1. User enters environmental values (N, P, K, temperature, humidity, pH, rainfall)  
2. Data is sent to the backend  
3. ML model processes the input  
4. System returns the most suitable crop  

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
