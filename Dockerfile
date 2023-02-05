FROM python:3.9.16-slim

COPY . /app
WORKDIR /app

# Create the virtual environment and install all the dependencies
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install pip --upgrade pip && /opt/venv/bin/pip install wheel &&  \
    /opt/venv/bin/pip install -r requirements.txt

# Engage the application entrypoint and run the application server
RUN chmod +x entrypoint.sh
CMD ["/app/entrypoint.sh"]



