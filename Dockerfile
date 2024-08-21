# Utilise une image légère de Python 3.11 comme base
FROM python:3.11-slim

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie tous les fichiers du répertoire courant sur la machine hôte vers le répertoire de travail dans le conteneur
COPY . .

# Installe les dépendances listées dans le fichier requirements.txt sans utiliser le cache pour minimiser la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Indique que le conteneur écoutera sur le port 5001
EXPOSE 5001

# Définit la commande par défaut à exécuter lorsque le conteneur démarre : lance l'application Flask
CMD ["python", "app.py"]
