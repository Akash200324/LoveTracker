# 💖 Couple Tracker - The Ultimate Relationship App 💖

<div align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" alt="Django" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="JavaScript" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="HTML5" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" alt="CSS3" width="40" height="40"/>
  
  <h3><strong>Track, Cherish, and Grow Your Love!</strong></h3>
  
  <!-- 3D Animation Placeholder - Replace the src link below with your favorite 3D GIF or Animation from Giphy or an Asset you create -->
  <img src="https://i.pinimg.com/originals/18/bf/7a/18bf7a342416f4061a9cb99a18413a2a.gif" alt="3D Heart Animation" width="300" style="border-radius: 20px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);"/>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  </p>

  <p>
    <a href="#about-the-project">About</a> •
    <a href="#features">Features</a> •
    <a href="#how-it-works">How It Works</a> •
    <a href="#tech-stack">Tech Stack</a>
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
