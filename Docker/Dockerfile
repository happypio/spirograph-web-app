FROM python:3.10-slim

WORKDIR /app

COPY app.py .
COPY src/ ./src/
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]