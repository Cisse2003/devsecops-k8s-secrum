# Build
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .

# Installation des dépendances dans le répertoire utilisateur du builder
RUN pip install --user --no-cache-dir -r requirements.txt


# Runtime
FROM python:3.11-slim
WORKDIR /app

# Mise à jour directe des paquets système Python vulnérables dans l'image finale
RUN pip install --no-cache-dir --upgrade pip "wheel>=0.45.1" "jaraco.context>=5.3.0"

# Création de l'utilisateur non privilégié
RUN addgroup --gid 10001 appuser && \
    adduser --uid 10001 --ingroup appuser --disabled-password --shell /bin/false appuser

# Copie des dépendances compilées depuis le Build (FIX: /home/appuser/.local avec le point)
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .

# Mettre à jour les permissions pour l'utilisateur appuser
RUN chown -R appuser:appuser /home/appuser/.local /app

ENV PATH=/home/appuser/.local/bin:$PATH

USER 10001

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]