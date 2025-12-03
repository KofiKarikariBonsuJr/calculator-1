Run local tests:
pip install -r requirements.txt
pytest

Run locally with docker
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
export DATABASE_URL=postgresql+psycopg2://john:pwd0123456789@localhost:5432/mydbs
pytest -q
