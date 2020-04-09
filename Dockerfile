FROM ubuntu:latest

WORKDIR /app

COPY . /app

### 2. Get Java via the package manager
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    apt-get install -y default-jdk && \
    apt-get clean

### 3. Get Python, PIP

RUN apt-get install -y python3.7 && \
    apt-get install -y python3-venv python3-pip && \
    pip3 install -r requirements/requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py"]