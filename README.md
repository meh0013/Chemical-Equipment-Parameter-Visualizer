# Chemical Equipment Parameter Visualizer  
**Hybrid Web + Desktop Application**

## 📌 Project Summary

The **Chemical Equipment Parameter Visualizer** is a hybrid data visualization and analytics application that runs as both a **Web Application** and a **Desktop Application**.  
It allows the user to upload CSV files containing chemical equipment data, perform analysis, and visualize results through charts and a downloadable summary report.

The system uses a **common Django REST API backend**, consumed by:
- a **React.js Web Dashboard**
- a **PyQt5 Desktop Application**

## 🧪 Project Overview

Users can upload CSV files with the following columns:

- Equipment Name  
- Equipment Type  
- Flowrate  
- Pressure  
- Temperature  

The backend processes the data using **Pandas**, computes statistics, stores recent uploads, and declares the results via REST APIs.  
Both frontends visualize this data using charts and tables.

## 🏗️ Architecture

### 🧰 Tech Stack

| Layer | Technology | Purpose |
|------|-----------|--------|
| Web Frontend | React.js + Chart.js | Tables & charts |
| Desktop Frontend | PyQt5 + Matplotlib | Desktop visualization |
| Backend | Django + Django REST Framework | REST APIs |
| Data Handling | Pandas | CSV analytics |
| Database | SQLite | Store last 5 datasets |
| Auth | JWT (SimpleJWT) | Secure API access |
| Version Control | Git & GitHub | Collaboration |

## ✨ Key Features

- CSV Upload via Web & Desktop
- Data summary API (counts, averages, distributions)
- Chart visualization (Web & Desktop)
- Store last 5 uploaded datasets
- PDF report generation
- JWT-based authentication
- Demo user auto-created for testing

## 📁 Sample Data

A sample CSV file is included:

## 🚀 Setup Instructions

### 🔧 Prerequisites

Ensure the following are installed on your system:

- Python **3.9+**
- Node.js **18+**
- npm (comes with Node.js)
- Git

 All required Python packages for the backend and desktop application are listed in their respective `requirements.txt` files and will be installed during setup.


##  Backend Setup (Django)

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
The backend runs at http://127.0.0.1:8000/

## Web Frontend Setup

```bash
cd web-frontend
npm install
npm start
```
The backend runs at http://localhost:3000/

## Desktop Frontend Setup

```bash
cd desktop-app
pip install -r requirements.txt
python main.py
```
The backend runs at http://localhost:3000/

Make sure the Django backend is running before starting the desktop app.

## 🌍 Deployment (Web Version)

### Defaults

```
USERNAME: demo
PASSWORD: 123123
``` 

- **Backend API**: https://fossee-chemical-equipment-parameter.onrender.com
- **Web Application**: https://fossee-chemical-equipment-parameter.vercel.app/

Note: The backend is hosted on a free-tier service and may take a few seconds to wake up on first request.
