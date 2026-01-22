![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![React Native](https://img.shields.io/badge/react_native-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

# 🥗 Calorie Tracker App

A professional, full-stack nutritional management and body progress tracking system. This project demonstrates a robust backend architecture using **FastAPI** and a highly responsive mobile experience built with **React Native (Expo)**.

---

## 🚀 Key Features

* **Personalized "Fridge" System:** Manage a custom database of products and complex meals.
* **Granular Daily Logging:** Track intake across categories (Breakfast, Lunch, Dinner, Snacks) with a real-time calorie/macro countdown.
* **Dynamic TDEE Calculation:** Nutritional goals are automatically calculated based on age, gender, activity level, and weight-loss velocity.
* **Body Metrics & Progress:** Integrated weight and body part measurements with historical logs and **Interactive Progress Charts**.
* **Smart Overwrite Protection:** Intelligent "Upsert" logic for daily measurements with user confirmation alerts.
* **Seamless UX:** Full support for **Dark & Light modes**, optimized for system-wide user preferences.

---

## 🛠 Technical Highlights

### **Backend (Domain-Driven Design)**
* **Architecture:** Clean architecture following **DDD principles** (Routers -> Services -> Repositories).
* **Dependency Injection:** Full utilization of FastAPI's DI system for user, database sessions, repositories, and services.
* **Security Layer:** * Dual-token system (**JWT Access + Refresh Tokens**).
    * **Redis** integration for session management, token storage, and rate-limiting (Auth).
    * Password security using **Argon2** hashing.
* **Data Integrity:** Pydantic V2 for strict validation and Alembic for automated database migrations.
* **Optimization:** Custom exception handlers and optimized SQLAlchemy queries to prevent N+1 problems.
* **Testing & Quality:** *Robust test suite powered by `pytest`, ensuring business logic reliability.
* **CI/CD Pipeline:** Automated testing and code quality checks via **GitHub Actions** on every Pull Request.
* **Code Quality:** Backend linting and formatting enforced by **Ruff**.

### **Frontend (Performance First)**
* **State Management:** Optimized UI with **Optimistic Updates** for an instant feel during data entry/deletion.
* **Efficient Data Handling:** Client-side filtering for the "Fridge" items to reduce server load and improve search speed.
* **Network Layer:** Axios with custom **Interceptors** for automated token refreshing and secure header injection.
* **Storage:** Sensitive data managed via **Expo SecureStore**.
* **Performance:** Strategic use of `useMemo` and `useCallback` to minimize redundant re-renders and heavy calculations.

---

## 🏗 Infrastructure
* **Dockerized Environment:** Fully containerized Backend, PostgreSQL, and Redis using **Docker Compose**.
* **Multi-environment Support:** Architecture prepared for `Test`, `Dev`, and `Prod` stages using Pydantic `BaseSettings`. 
* **Configuration:** Template provided via `.env.example` for secure and flexible environment management.

---

## 📸 Screenshots & Demo

|          Nutrition Logs          |            Profile             |       Progress Charts        |
|:--------------------------------:|:------------------------------:|:----------------------------:|
| ![Screen1](images/meal-logs.jpg) | ![Screen2](images/profile.jpg) | ![Screen3](images/chart.jpg) |

|           Fridge (Products)            |          Body Measurements          |           Body & goals            |
|:--------------------------------------:|:-----------------------------------:|:---------------------------------:|
| ![Screen4](images/fridge-products.jpg) | ![Screen5](images/measurements.jpg) | ![Screen6](images/body-goals.jpg) |

> ### 🎥 **Watch the full App Demo on LinkedIn:** [Demo](https://www.linkedin.com/feed/update/urn:li:activity:7419329394672009217/)

---

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/mtrznadel24/calorie-tracker-app.git](https://github.com/mtrznadel24/calorie-tracker-app.git)
    cd calorie-tracker-app
    ```

2.  **Infrastructure Setup (Backend & DB):**
    ```bash
    cd FastAPI
    # Setup your .env file
    docker-compose up --build
    ```
    
3. **Run database migrations**
    ```bash
    # In a new terminal, run migrations
    docker exec -it calorie-tracker-api alembic upgrade head
    ```

> ⚠️ Note: If you have a local Python environment configured with Poetry, you can also run poetry run alembic upgrade head.

4. **Frontend Setup:**
    ```bash
    cd ReactNative
    npm install
    # Create a .env file in the ReactNative folder and provide your local IP address
    npx expo start
    ```

> ⚠ TIP: How to find your local IP?

Windows: Run ipconfig in CMD/PowerShell and look for IPv4 Address (usually 192.168.x.x).

macOS/Linux: Run ifconfig or hostname -I.   
> ⚠️ IMPORTANT: If you are on a public/restricted Wi-Fi network and can't connect, try running with the tunnel flag: npx expo start --tunnel


---

## 👨‍💻 Author

* **Maciej Trznadel** – *AGH University of Krakow*
* **Github:** [@mtrznadel24](https://github.com/mtrznadel24)
* **LinkedIn:** [Maciej Trznadel](https://www.linkedin.com/in/mtrznadel24/)

---
