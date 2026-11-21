FROM node:24-alpine AS frontend
WORKDIR /web
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt backend/constraints-py312.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt -c backend/constraints-py312.txt
COPY backend/ ./backend/
COPY --from=frontend /web/dist ./frontend/dist
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8010
CMD ["python", "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8010"]
