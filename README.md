# Extraordinary - Django Landing Site (Creative & Animated)

This is a starter Django project for the Facebook page **"Extraordinary"** — a creative, animated, mobile-first landing site using Tailwind via CDN.

Features included:
- Landing page with animated hero, About, Featured (admin-posted) videos/posts (mock), Contact / Social links, Newsletter signup (admin-viewed), and Footer.
- Admin interface to create Featured posts and Videos and view newsletter signups.
- Responsive design optimized for mobile devices.
- Tailwind CSS used via CDN (for simplicity). Replace with Tailwind CLI or integration for production if desired.
- SQLite for quick local setup. Deployment-ready settings notes included.

## Quick setup (local)
1. Create a virtualenv and activate it.
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

## Deploy
- This project is intentionally simple to deploy (e.g., Render, Vercel for Django, or any VPS).
- For production: set DEBUG=False, configure ALLOWED_HOSTS, add static files handling (WhiteNoise or cloud storage), and secure SECRET_KEY.

