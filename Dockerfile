FROM continuumio/miniconda3:4.6.14

RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisord.conf

RUN pip install pyuwsgi==2.0.18 supervisor==4.0.3

# First copy only requirements.txt, to cache dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Then copy the rest of the files
COPY . .

# Use production mode
RUN sed -i.bak "s|DEBUG = True|DEBUG = False|" app/settings.py

EXPOSE 80
CMD ["supervisord", "-n"]
