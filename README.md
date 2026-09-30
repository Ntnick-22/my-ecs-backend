# myecs-backend

Flask REST API (served by gunicorn on port 8000) backed by PostgreSQL. Backend tier of a three-tier app running on AWS ECS Fargate — infrastructure lives in `aws_ecs_infra`.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | API status + database connectivity |
| GET | `/api/users` | List registered users |
| GET | `/api/stats` | User / role counts |
| POST | `/api/register` | Register a user (`name`, `email`, `role`) |
| DELETE | `/api/users/<id>` | Delete a user |

## Configuration

All configuration comes from environment variables: `DB_HOST`, `DB_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.

## Run locally

Create a `.env` file (git-ignored):

```
FLASK_ENV=development
BACKEND_PORT=8000
DB_PORT=5432
POSTGRES_DB=learn_devops
POSTGRES_USER=learn_user
POSTGRES_PASSWORD=localdev123
```

Then:

```bash
docker compose up --build -d
curl localhost:8000/api/health
```
