FROM python:3.11-slim

WORKDIR /employee-project

COPY requirement.txt .
RUN pip install -r requirement.txt
COPY . .
RUN pip install flask
CMD ["python", "app.py"]
