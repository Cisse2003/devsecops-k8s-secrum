# Build

FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .

# Installation des dépendances dans le répertoire utilisateur pour ne pas polluer l'image globale
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime
FROM python:3.11-slim
WORKDIR /app

# Création d'un groupe et d'un user système non privilégié (UID/GID 10001)
# l'option -s /bin/false empêche 'louverture d'un shell interactif par défaut

# ANCIENNE VERSION (qui échoue) :
#RUN groupadd -g 10001 appuser && \ useradd -u 10001 -g appsuer -s /bin/false appsuer

# NOUVELLE VERSION (compatible Debian slim) :
RUN addgroup --gid 10001 appuser && \
    adduser --uid 10001 --ingroup appuser --disabled-password --shell /bin/false appuser

# copie des dependances compilées depuis le Build
COPY --from=builder /root/.local /home/appuser.local
COPY app.py .

# Mettre a jour le path pour executer gunicorn
ENV PATH=/home/appuser/.local/bin:$PATH

# user non root
USER 10001

EXPOSE 5000

# Healthcheck pour verifier l'etat du serveur Flask/Gunicorn
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# serveur WSGI de gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
