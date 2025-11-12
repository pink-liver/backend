FROM python:3.11-slim

WORKDIR /app

ENV TZ=Asia/Taipei

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project code
COPY . .

EXPOSE 8080

# environment variables
ENV FLASK_APP=main.py

# run the application
CMD ["python", "main.py"]
