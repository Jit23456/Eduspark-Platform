# EduSpark Platform

EduSpark is a Django learning platform with course pages, embedded video lectures, and exam support.

## Live App

- Public app: https://eduspark-live-25047.azurewebsites.net/
- Courses page: https://eduspark-live-25047.azurewebsites.net/courses/

## What is included

- Class and subject-based course catalog
- Course detail pages with chapter sections
- YouTube video lecture embedding
- SQLite database for local development
- Azure App Service configuration in `.azure/config`

## New Class 10 lecture

This project now seeds a Class 10 course and featured lecture through the migration:

- `eduspark/courses/migrations/0003_seed_class10_featured_lecture.py`

The seeded lecture uses this YouTube URL:

- `https://youtu.be/Z_e0ToEM8XU?si=y5-ExEsTL66aBNOo`

## Local run

From the project root:

```powershell
cd "C:\Users\HP\Dropbox\My PC (LAPTOP-MO4VABTT)\Desktop\eduspark platform\eduspark"
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

Open locally at:

- `http://127.0.0.1:8000`

## Public access with ngrok

Keep Django running, then in a second terminal from the workspace root:

```powershell
cd "C:\Users\HP\Dropbox\My PC (LAPTOP-MO4VABTT)\Desktop\eduspark platform"
.\venv\Scripts\ngrok.exe http 8000
```

Open the `https://...ngrok-free.app` URL printed by ngrok.

## Azure deployment notes

This repo already contains Azure App Service settings:

- Resource group: `eduspark-rg`
- Plan: `surajitchakraborty823_asp_9657`
- Location: `southindia`
- Web app: `edusparkplatformapp6839`

To deploy from a machine that is logged into Azure CLI:

```powershell
cd "C:\Users\HP\Dropbox\My PC (LAPTOP-MO4VABTT)\Desktop\eduspark platform\eduspark"
az webapp up --name edusparkplatformapp6839 --resource-group eduspark-rg --plan surajitchakraborty823_asp_9657 --location southindia
```

If static assets are missing after deployment, run:

```powershell
..\venv\Scripts\python.exe manage.py collectstatic --noinput
```

## GitHub push checklist

This folder is not currently a Git repository, so initialize and connect it before pushing:

```powershell
cd "C:\Users\HP\Dropbox\My PC (LAPTOP-MO4VABTT)\Desktop\eduspark platform\eduspark"
git init
git add .
git commit -m "Add Class 10 featured lecture and deployment docs"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Notes

- The Class 10 lecture title and duration are seeded with safe defaults.
- You can refine the lecture metadata later from Django admin or a follow-up migration.
