# 🚀 LLM DevOps Assistant

> **AI-Powered CI/CD Automation & Build Log Intelligence Platform**  
> Streamline continuous integration by marrying **Jenkins**, **Django**, **PostgreSQL**, and **Google Gemini AI** to automatically capture build failures, diagnose root causes, and prescribe remediation steps in real time.

---

[![Django](https://img.shields.io/badge/Django-6.0%2B-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Generative%20AI-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

---

## 📌 Overview

Modern DevOps teams lose countless engineering hours reading through thousands of lines of verbose Jenkins console logs to decipher why a build failed.

**LLM DevOps Assistant** bridges Jenkins CI/CD execution and generative AI to deliver instantaneous, actionable insights. Whenever a build triggers or fails in Jenkins:
1. The raw console logs and pipeline metadata are delivered securely via REST API to Django.
2. The **Google Gemini AI Engine** synthesizes the execution trace, isolating the exact failure from noisy warnings.
3. The platform generates an executive **Root Cause**, **Build Summary**, and **Step-by-Step Suggested Fix**.
4. Results update live on an interactive web dashboard with KPI cards, analytics, and build duration metrics.

---

## 🏗️ System Architecture

```mermaid
graph LR
    subgraph CI_CD [CI/CD Environment]
        Developer([🧑‍💻 Developer]) -->|git push| GitHub([🐙 GitHub Repo])
        GitHub -->|Webhook / Poll| Jenkins[⚙️ Jenkins CI/CD Engine]
        Jenkins -->|Runs Pipeline| Runner[📦 Docker Build Runner]
        Runner -->|send_build.py| Webhook[📡 Build Webhook Payload]
    end

    subgraph Backend [Django Web Application]
        Webhook -->|POST /api/builds/ (Token Auth)| DjangoAPI[🛡️ REST API Layer]
        DjangoAPI --> BuildService[⚙️ Build Processor]
        BuildService --> AIEngine[🧠 Gemini AI Engine]
        BuildService --> DB[(🗄️ PostgreSQL Database)]
        AIEngine -->|Generates Root Cause & Fix| BuildService
    end

    subgraph Client [Web Dashboard]
        User([🧑‍💼 DevOps Engineer / SRE]) <-->|Live Polling & UI| Dashboard[📊 Real-Time Analytics Dashboard]
        Dashboard <-->|Query Builds & KPIs| DjangoAPI
    end
```

---

## ✨ Key Features

- **🤖 Automated AI Root Cause Analysis**: Identifies syntax errors, missing dependencies, database connection dropouts, or test failures without manual log inspection.
- **⚡ Real-Time Dashboard Updates**: Auto-refreshing KPI metrics (Total Builds, Success Rate, Failure Count, Average Duration) powered by lightweight asynchronous AJAX polling.
- **🔄 Dynamic Jenkins Pipeline Management**: Create, edit, and trigger multiple Jenkins pipelines directly from the Django web UI with one click.
- **📂 Multi-Project Organization**: Group pipelines and builds under specific projects with Git branch tracking and commit monitoring.
- **📈 Comprehensive Reports & Analytics**: Interactive charts powered by Chart.js displaying build trends, success distributions, and duration tracking.
- **🛡️ Secure Token-Based API**: Hardened endpoint authentication via Django REST Framework tokens (`TokenAuthentication`) for webhook payloads.
- **🐳 Cloud & Container Ready**: Pre-configured `docker-compose.yml` for PostgreSQL, custom Jenkins Dockerfile with plugins pre-installed, and automated deployment scripts (`build.sh`, `render.yaml`, `Procfile`) for Render / Railway.

---

## 🛠️ Tech Stack

| Domain | Technologies |
|---|---|
| **Backend Framework** | Django 6.0, Django REST Framework (DRF), Gunicorn, Whitenoise |
| **Artificial Intelligence** | Google Gemini API (`google-genai` SDK), prompt-engineered DevOps analysis |
| **Database & Cache** | PostgreSQL 16, `psycopg` 3.x, `dj-database-url` |
| **DevOps & CI/CD** | Jenkins (Declarative Pipeline `Jenkinsfile`), Docker Desktop, Docker Compose |
| **Frontend & UI** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js |
| **Cloud Deployment** | Render, Railway, Linux / Systemd |

---

## 📂 Repository Structure

```text
llm-devops-assistant/
├── backend/                        # Django Application Root
│   ├── ai_engine/                  # Gemini AI integration service & prompts
│   ├── api/                        # REST framework API views and routing
│   ├── builds/                     # Build models, serializers & detail views
│   ├── config/                     # Core Django settings, WSGI, ASGI, URLs
│   ├── dashboard/                  # KPI dashboard, analytics & reports views
│   ├── pipeline/                   # Pipeline CRUD & Jenkins trigger services
│   ├── projects/                   # Project models, forms & management views
│   ├── scripts/                    # Helper scripts (send_build.py, fetch_console_log.py)
│   ├── static/                     # CSS, JavaScript & theme assets
│   ├── users/                      # Authentication (Login, Register, Logout)
│   ├── manage.py                   # Django CLI entrypoint
│   └── requirements.txt            # Python dependencies
├── docker/
│   └── jenkins/                    # Jenkins Dockerfile & required plugins
├── docs/                           # Architecture, API & Database documentation
├── scripts/                        # Jenkins connection testing utilities
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignored files & static directories
├── build.sh                        # Render / Cloud build & migration script
├── docker-compose.yml              # PostgreSQL container configuration
├── Procfile                        # Cloud process starter (Gunicorn)
├── render.yaml                     # Infrastructure-as-Code for Render deployment
├── requirements.txt                # Root dependencies list
└── README.md                       # Project documentation
```

---

## 🚀 Quickstart Guide (Local Development)

### 1. Prerequisites

Ensure you have the following installed on your local workstation:
- **Python 3.11+** (Python 3.13 recommended)
- **Docker Desktop** & **Docker Compose**
- **Git**
- A **Google Gemini API Key** ([Get one at Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository

```bash
git clone https://github.com/sopparapupraneethkumar-hub/llm-devops-assistant.git
cd llm-devops-assistant
```

### 3. Setup Virtual Environment

```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create your local `.env` file from the provided template:

```bash
# Windows PowerShell
Copy-Item .env.example backend\.env

# Linux / macOS
cp .env.example backend/.env
```

Edit `backend/.env` with your secrets:

```ini
SECRET_KEY=django-insecure-your-local-secret-key-change-in-prod
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://postgres:postgres123@localhost:5433/llm_devops_db
GEMINI_API_KEY=your_actual_gemini_api_key_here

JENKINS_URL=http://localhost:8080
JENKINS_USER=admin
JENKINS_API_TOKEN=your_jenkins_api_token_here
DJANGO_API_TOKEN=your_django_rest_auth_token_here
```

### 6. Start PostgreSQL with Docker

```bash
docker compose up -d
```

Verify that the `llm_postgres` container is running and healthy on port `5433`.

### 7. Run Database Migrations & Create Superuser

```bash
python backend/manage.py migrate
python backend/manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python backend/manage.py runserver 8000
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## ⚙️ Jenkins CI/CD Setup

### 1. Run Jenkins with Docker

Build and start the custom Jenkins container containing Python, virtualenv, and required plugins:

```bash
docker build -t custom-jenkins -f docker/jenkins/Dockerfile .
docker run -d --name custom_jenkins -p 8080:8080 -p 50000:50000 custom-jenkins
```

### 2. Configure Credentials in Jenkins

1. Go to **Manage Jenkins** → **Credentials** → **System** → **Global credentials**.
2. Add **Username with password** credential:
   - **ID**: `jenkins-api`
   - **Username**: Your Jenkins username (e.g., `admin`)
   - **Password**: Your Jenkins API Token generated from your profile

### 3. Pipeline Workflow

The repository includes a battle-tested `backend/Jenkinsfile` that:
1. Sets up the Python virtual environment and installs dependencies.
2. Executes Django system check verification (`python manage.py check`).
3. Under the `post` block, automatically executes `backend/scripts/send_build.py` to extract the build console log and dispatch it to the Django REST endpoint with the authentication token.

---

## ☁️ Deployment Guide (Render)

This repository is pre-configured for one-click deployment to **Render** using `render.yaml` or Render's Web Service dashboard.

### Render Web Service Settings

| Configuration Option | Value |
|---|---|
| **Environment** | `Python` |
| **Root Directory** | `.` (or empty) |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn --chdir backend config.wsgi:application` |

### Required Environment Variables on Render

| Variable | Description | Example |
|---|---|---|
| `PYTHON_VERSION` | Python runtime version | `3.13.1` |
| `SECRET_KEY` | Production Django secret key | Auto-generated or custom string |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@host/db` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `JENKINS_URL` | Public / Accessible Jenkins URL | `https://jenkins.yourdomain.com` |
| `JENKINS_USER` | Jenkins administrator user | `admin` |
| `JENKINS_API_TOKEN` | Jenkins API user token | `11...` |

---

## 📡 REST API Reference

### 1. Submit Build Log & Trigger AI Analysis

- **Endpoint**: `POST /api/builds/`
- **Authentication**: `Authorization: Token <DJANGO_API_TOKEN>`
- **Content-Type**: `application/json`

**Sample Request Payload:**
```json
{
  "jenkins_job_name": "production-service-pipeline",
  "build_number": 42,
  "project_name": "production-service-pipeline",
  "branch": "main",
  "status": "FAILURE",
  "duration": 48,
  "console_log": "django.core.exceptions.ImproperlyConfigured: ...\nFinished: FAILURE"
}
```

**Sample Response (`200 OK`):**
```json
{
  "message": "Build processed successfully",
  "data": {
    "id": 15,
    "build_number": 42,
    "project_name": "production-service-pipeline",
    "branch": "main",
    "status": "FAILURE",
    "duration": 48,
    "ai_summary": "Root Cause:\n- Missing environment variable in production settings.\n\nSummary:\n- Build failed during Django initialization.\n\nSuggested Fix:\n1. Verify SECRET_KEY is supplied in production environment.\n2. Re-run deployment pipeline.",
    "created_at": "2026-09-19T11:42:00Z"
  }
}
```

### 2. Projects API

- **List / Create Projects**: `GET` / `POST` `/projects/api/`

---

## 🤝 Contributing

Contributions, feature requests, and bug reports are warmly welcome!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'feat: Add AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ using Django, Jenkins, PostgreSQL, and Google Gemini AI.</sub>
</div>

