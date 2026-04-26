FROM python:3.11-slim
WORKDIR /app
COPY triage_wars/server/requirements.txt .
RUN pip install -r requirements.txt
COPY triage_wars/ ./triage_wars/
COPY triage_wars/server/app.py .
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]