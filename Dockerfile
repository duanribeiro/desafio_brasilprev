FROM python:3.7-stretch as base

FROM base as builder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local

COPY . /app

WORKDIR /app

EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b :5000", "-w 3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "run:app"]