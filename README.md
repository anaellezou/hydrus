# 水蛇座 Hydrus

![CI](https://github.com/anaellezou/hydrus/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/anaellezou/hydrus/actions/workflows/cd.yml/badge.svg)

A minimalist JLPT study app — browse kanji, vocabulary, and grammar from N5 to N1.

---

## Stack

**Backend** — Python · Flask · SQLite · Docker  
**Frontend** — React · Vite · Styled Components  
**Infrastructure** — Terraform · AWS EC2 · Docker Compose  
**CI/CD** — GitHub Actions

---

## Run locally

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Setup

```bash
git clone https://github.com/anaellezou/hydrus.git
cd hydrus
```

Create the environment files:

```bash
# frontend/.env
echo "VITE_API_BASE=http://localhost:5001/api" > frontend/.env

# backend/.env
echo "SECRET_KEY=your_secret_key_here" > backend/.env
echo "FRONTEND_URL=http://localhost:5173" >> backend/.env
```

Launch:

```bash
docker compose up --build
```

The app will be available at **http://localhost:5173**  
The database is created automatically on first launch.

---

## Infrastructure

The app is deployed on AWS EC2 and provisioned with Terraform.

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install)
- [AWS CLI](https://aws.amazon.com/cli/) configured with `aws configure`
- An SSH key pair at `~/.ssh/hydrus`

### Provision infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Start / stop the instance

```bash
# Start
./start.sh

# Stop
./stop.sh
```

The `start.sh` script starts the EC2 instance, waits for it to be ready, and prints the app URL.

---

## CI/CD

Every push to `main` triggers the pipeline:

1. **CI** — runs pytest on the backend
2. **CD** — deploys to EC2 automatically if tests pass

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/kanji/?level=N5` | List kanji, filter by level |
| GET | `/api/kanji/<id>` | Get kanji by ID |
| GET | `/api/vocabulary/?level=N5` | List vocabulary, filter by level |
| GET | `/api/vocabulary/<id>` | Get vocabulary by ID |
| GET | `/api/grammar/?level=N5` | List grammar points, filter by level |
| GET | `/api/grammar/<id>` | Get grammar point by ID |

---

## Project Structure

```
hydrus/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── kanji/
│   │   │   ├── vocabulary/
│   │   │   └── grammar/
│   │   ├── database/
│   │   └── resources/
│   ├── tests/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── public/
│   └── Dockerfile
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── start.sh
├── stop.sh
└── docker-compose.yml
```

---

## Environment Variables

Create the following files locally (never commit them):

**`frontend/.env`**
```
VITE_API_BASE=http://localhost:5001/api
```

**`backend/.env`**
```
SECRET_KEY=your_secret_key_here
FRONTEND_URL=http://localhost:5173
```

## Next steps

- /!\ make it available for any kind of device /!\
- Add monitoring and alerting (Prometheus / Grafana or Datadog)
- Add staging environment
- Set up security scanning in the CI pipeline

- Review architecture to add other levels (N4 to N1)
- Add JLPT exams
- Add users and authentication (OAuth2 / JWT)
