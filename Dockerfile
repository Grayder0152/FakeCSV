FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN python -m pip install -r requirements.txt
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]