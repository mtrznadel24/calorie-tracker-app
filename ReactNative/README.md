# Calorie Tracker - Mobile App (React Native)

This is the frontend of the Calorie Tracker application, built with **React Native** and **Expo**. It provides a smooth, native experience for tracking nutrition and physical progress, with a strong emphasis on performance and clean UI/UX.

---

## Frontend Highlights

* **Efficient State Management:** To ensure a fast feel, the app utilizes localized state updates. Instead of reloading the entire dataset, only the relevant part of the UI is re-rendered after a successful server response.
* **Responsive Design:** Fully adaptive layouts built with **NativeWind (Tailwind CSS)**, supporting both **Dark and Light modes** based on system preferences.
* **Interactive Data Visualization:** Custom-styled charts powered by `react-native-gifted-charts` to track weight trends and body measurements.
* **Smart Navigation:** Utilizes **Expo Router** for file-based routing, ensuring a clean and intuitive navigation flow.

---

## Tech Stack

* **Framework:** React Native (Expo)
* **Language:** TypeScript (Strictly typed)
* **Styling:** NativeWind (Tailwind CSS)
* **API Client:** Axios with custom Interceptors
* **State & Logic:** React Hooks
* **Charts:** React Native Gifted Charts
* **Icons:** Lucide React & Material Community Icons
* **Storage:** Expo SecureStore (for sensitive token management)

---

## Network & Security Layer

One of the core features of the frontend is its robust communication with the FastAPI backend:

* **Axios Interceptors:** Automated handling of **Access & Refresh Tokens**. The app automatically attempts to refresh the session when a 401 error occurs, providing a seamless experience for the user.
* **Secure Storage:** JWT tokens are never stored in plain text; they are managed via **Expo SecureStore** for hardware-encrypted security.
* **Type Safety:** Shared interfaces between the backend and frontend ensure that all API responses are correctly typed and handled.

---

## Project Structure

```text
ReactNative/
├── api/                # Axios instance
├── app/                # Expo Router (Pages & Layouts)
├── components/         # Reusable UI components (Modals, Cards, Inputs)
├── services/           # API calls and Axios configuration
├── constants/          # Colors, Theme definitions, and API Endpoints
├── contexts/            # React Context for Auth and Global State
├── hooks/              # Custom hooks for logic reuse
├── assets/             # Images, fonts, and icons
└── .env.example        # Environment variables template
```

## Key Developer Features
* **Memoization:** Strategic use of useMemo and useCallback to prevent unnecessary re-renders in complex lists (like the "Fridge" or "Logs").

* **Clean Components:** Separation of business logic (Services/Hooks) from the presentation layer (Components).

## Getting Started

1. Requirements
Node.js (LTS)

Expo Go app on your phone or an Emulator (Android Studio / Xcode)

2. Installation
```bash
# Install dependencies
npm install
```

3. Configuration
```bash
# Create your environment file
cp .env.example .env
# Update EXPO_PUBLIC_API_URL with your local IP (e.g., [http://192.168.1.](http://192.168.1.)XX:8000)
```

4. Running the app
```bash
# Start the Expo server
npx expo start
```

```bash
# Pro tip: If your phone cannot connect to your computer via local Wi-Fi, 
# use the tunnel flag to bypass network restricti ASons:
npx expo start --tunnel
```

## UI/UX Features
Dynamic Theming: Dark and Light mode based on device settings.

Feedback System: Integrated Toast notifications for successful actions and error handling.

Anatomical Icons: Context-aware icons for body measurements (Material Community Icons).
