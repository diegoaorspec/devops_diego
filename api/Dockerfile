FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY notes ./notes

# La app escribe su log en /var/log/notes/app.log (fijo en config.py).
# Se enlaza a stdout para verlo con docker/kubectl logs. Usuario no-root.
RUN useradd -m app \
 && mkdir -p /var/log/notes \
 && ln -s /dev/stdout /var/log/notes/app.log \
 && chown -R app /var/log/notes
USER app

ENV MONGO_URI=mongodb://localhost:27017/notes
EXPOSE 5000

# MONGO_URI está fijo en config.py: se pasa a la factory create_app(overrides).
CMD ["sh", "-c", "exec gunicorn -b 0.0.0.0:5000 -w 2 --access-logfile - \"notes:create_app({'MONGO_URI': '$MONGO_URI'})\""]
