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

RUN groupadd -g 10001 appuser && \ useradd -u 10001 -g appsuer -s /bin/false appsuer

# copie des dependances compilées depuis le Build
COPY --from=builder /root/.local /home/appuser.local
COPY app.py .

# Mettre a jour le path pour executer gunicorn
ENV PATH=/home/appuser/.local/bin:$PATH

# user non root
USER 10001

EXPOSE 5000
# serveur WSGI de gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
