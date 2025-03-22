
# Phase 4: Docker Deployment

## Files
- `Dockerfile`
- `docker-compose.yml`

## Steps
1. Clone the project and add `.env` file with:

```env
OPENAI_API_KEY=your-api-key
```

2. Build and run:

```bash
docker-compose up --build
```

3. App is available at: http://localhost:8501
