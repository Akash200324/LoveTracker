# 💖 Couple Tracker - The Ultimate Relationship App 💖

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=30,ff5e62,ff9966&height=180&section=header&text=Couple%20Tracker&fontSize=50&animation=twinkling" width="100%"/>

  <br/>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white" />
    <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
  </p>

  <h3><strong>✨ Track, Cherish, and Grow Your Love Live! ✨</strong></h3>

  <img src="https://i.pinimg.com/originals/18/bf/7a/18bf7a342416f4061a9cb99a18413a2a.gif" alt="3D Heart Animation" width="220" style="border-radius: 50%; box-shadow: 0 0 35px rgba(255, 94, 98, 0.8); margin: 15px 0; animation: pulse 2s infinite alternate;"/>

  <p align="center">
    <a href="#about-the-project"><b>📖 About</b></a> •
    <a href="#system-architecture--deep-dive"><b>🧠 Architecture</b></a> •
    <a href="#outstanding-features"><b>✨ Features</b></a> •
    <a href="#how-it-works"><b>⚙️ Workflow</b></a> •
    <a href="#local-installation--setup"><b>🚀 Installation</b></a> •
    <a href="#tech-stack--languages-used"><b>🛠 Tech Stack</b></a>
  </p>
</div>

---

## 📖 About The Project

**Couple Tracker** is an interactive, feature-rich web application built to bring couples closer. Whether you're tracking your shared goals, saving the most precious memories, aligning your moods, or just planning the next movie night, this application serves as your personal relationship digital diary!

With a beautifully designed UI, smooth functionality, and secure user authentication, Couple Tracker acts as your all-in-one private hub. 

---

## ✨ Outstanding Features

Discover a magical ecosystem crafted specifically for couples:

- 🔐 **Dual-End Authentication**: Secure sign-up, login (including Google OAuth), password resets, and OTP verifications to keep your data private and safe.
- 👩‍❤️‍👨 **Couple Connection System**: Create a couple profile and securely invite your partner to join your digital world.
- 📸 **Memory Lane & Snaps**: Upload cherished photos to your memory album, manage snapshots, and never lose a sweet moment. Cloudinary handles all media storage efficiently!
- 📅 **Milestone Tracking**: Never forget an anniversary or an important date! Add, edit, and visualize your relationship milestones.
- 😊 **Mood Sync**: A real-time Mood Tracker. Log your mood and see your partner's mood instantly. Better communication starts with knowing how the other feels!
- 🍿 **Movie & Review Tracker**: Plan your next binge! Add movies, write shared reviews, and rank your favorite films.
- 🎶 **Shared Playlists & Songs**: Connect and manage your favorite shared songs and playlists. Music connects hearts!
- 🎯 **Bucket List**: A dynamic checklist of everything you both want to accomplish together. Dream big and cross them off one by one!
- 🌸 **Period Tracker**: Built-in functionality specifically to stay aware and supportive.
- 🔔 **Push Notifications & Reminders**: Web push notifications (via pywebpush) and automated inactivity cron jobs ensure you are always engaged and reminded of your love.

---


## ⚙️ How It Works

### Application Architecture
```mermaid
graph TD
    %% Define styles for aesthetic
    classDef user fill:#FFE5EC,stroke:#FF4D6D,stroke-width:2px,color:#800F2F
    classDef server fill:#D8F3DC,stroke:#1B4332,stroke-width:2px,color:#081C15
    classDef db fill:#CAF0F8,stroke:#0077B6,stroke-width:2px,color:#03045E
    classDef cloud fill:#E0AAFF,stroke:#5A189A,stroke-width:2px,color:#240046
    classDef push fill:#FFF3B0,stroke:#E09F3E,stroke-width:2px,color:#540B0E

    UserA("👤 Partner A"):::user <-->|"HTTPS & Auth (Google/Session)"| Django["🚂 Django App Server (Vercel)"]:::server
    UserB("👤 Partner B"):::user <-->|"HTTPS & Auth (Google/Session)"| Django
    
    Django <-->|"Django ORM"| Postgres[("🐘 PostgreSQL Database")]:::db
    
    Django <-->|"Media Storage/Retrieval"| Cloudinary["☁️ Cloudinary CDN"]:::cloud
    Cloudinary -->|"Serves Optimized Media"| UserA
    Cloudinary -->|"Serves Optimized Media"| UserB
    
    Django -->|"PyWebPush Engine"| PushService["🔔 Browser Push Service (FCM/Apple)"]:::push
    PushService -->|"Triggers Service Worker"| UserA
    PushService -->|"Triggers Service Worker"| UserB
    
    Cron["⏰ Cron Jobs"]:::server -->|"Triggers Inactivity API"| Django
```

### User Flow

1. **Onboarding**: Users register for an account (Standard or via Google).
2. **Pairing**: A user creates a "Couple" and generates a link/code for their partner. Their partner joins, linking their accounts in the database.
3. **The Dashboard**: Once paired, both users land on a shared dashboard where they can interact with the various modules.
4. **Real-time Syncing**: As you upload a memory, add a movie, or update your mood, it reflects directly in your partner's dashboard seamlessly!

---

## 🛠 Tech Stack & Languages Used

This project relies on a robust set of modern technologies:

### 🎨 Frontend
- **HTML5 & CSS3**: For structural layout and beautiful custom styling.
- **JavaScript (Vanilla/ES6)**: To handle interactive UI, AJAX requests, DOM manipulation, Modal interactions, and Web Push Service Workers.
- *(Note: Embellished with beautiful typography via Google Fonts and crisp icons)*

### 🧠 Backend
- **Python (v3.x)**: The core programming language powering the logic.
- **Django (v5.0.6)**: A high-level Python web framework encouraging rapid development and clean design.
- **Authentication**: `google-auth` for seamless Google logins and Django's robust default authentication system.

### 🗄 Database & Storage
- **PostgreSQL**: Relational database handling structured data (Users, Couples, Movies, Reviews).
- **Cloudinary**: High-performance cloud storage for all couple images and memories.

### 🚀 Deployment & Utilities
- **Vercel**: `vercel.json`, `gunicorn`, `whitenoise`, and `dj-database-url` perfectly configured to deploy as a serverless or managed platform application.
- **Asynchronous/Push Services**: `pywebpush` and `py-vapid` for web push notifications.
- **Payments (Optional Module)**: `razorpay` integration included for any premium upgrade options.

---

<div align="center">
  <p><i>Made with ❤️ by AKASH</i></p>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=100&section=footer" width="100%"/>
</div>








