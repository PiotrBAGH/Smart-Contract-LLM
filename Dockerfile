# Użyj oficjalnego obrazu Python jako podstawy
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do katalogu roboczego
COPY . /app

# Zainstaluj wymagane biblioteki
RUN pip install --no-cache-dir -r requirements.txt

# Eksponuj port, na którym działa aplikacja Flask
EXPOSE 5000

# Dodaj katalog 'app' do PYTHONPATH
ENV PYTHONPATH=/app/app

# Ustaw zmienną środowiskową dla Flask
ENV FLASK_APP=app/app.py

# Uruchom aplikację
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
