FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# ===== Pre-descarga del modelo en tiempo de build =====
# Guardamos cache dentro de la imagen
ENV HF_HOME=/app/.cache/hf \
    TRANSFORMERS_CACHE=/app/.cache/hf

RUN python -c "from pysentimiento import create_analyzer; create_analyzer(task='sentiment', lang='es', model_name='pysentimiento/robertuito-sentiment-analysis')"

# Runtime: usar /tmp (escribible) y copiar cache si quieres, pero no es necesario
ENV HF_HOME=/tmp/hf \
    TRANSFORMERS_CACHE=/tmp/hf

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
