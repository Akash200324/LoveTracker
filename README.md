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

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4d6/512.webp" width="28" height="28"> 📖 About The Project

> [!NOTE]  
> **Couple Tracker** is an interactive, secure, private digital ecosystem built to eliminate physical distance and bridge emotional gaps between partners. Whether you are navigating a long-distance relationship or preserving daily memories under one roof, this application serves as a dedicated virtual home shared exclusively by two individuals.

Unlike generic social media networks, **Couple Tracker** emphasizes **absolute privacy, atomic 1:1 synchronization, and collaborative milestone tracking**. Powered by a robust Python/Django backend architecture, secure relational databases, and dynamic web asynchronous push networks, it records real-time moods, shared cinema lists, and lifecycle milestones inside an aesthetic, custom-engineered interface.

---

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f9e0/512.webp" width="28" height="28"> 🧠 System Architecture & Deep Dive

To ensure data sovereignty and rapid response cycles, the application breaks functions down across distinct decoupled operations:

```mermaid
graph TD
    UserA[👤 Partner A] <-->|HTTPS / Session Auth| Django[🚂 Django Application Server]
    UserB[👤 Partner B] <-->|HTTPS / Session Auth| Django
    Django <-->|ORM Dialect| Postgres[(🐘 PostgreSQL Database)]
    Django -->|Asynchronous Delivery Engine| WebPush[🔔 PyWebPush Service Worker]
    Django <-->|Media Engine Payload| Cloudinary[☁️ Cloudinary CDN]
    WebPush -->|Instant Alert| UserA
    WebPush -->|Instant Alert| UserB
