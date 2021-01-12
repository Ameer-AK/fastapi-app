FROM python:3-alpine

ARG EXTRA_REQUIREMENTS

ENV DB_USERNAME $DB_USERNAME
ENV DB_PASSWORD $DB_PASSWORD
ENV DB_HOSTNAME $DB_HOSTNAME
ENV DB_PORT $DB_PORT
ENV DB_NAME $DB_NAME

WORKDIR /app

ENV PYTHONPATH $PYTHONPATH:$(pwd)/src

RUN apk add --no-cache postgresql-libs bash && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev make

COPY requirements.txt .

COPY test-requirements.txt .

RUN pip install -r ${EXTRA_REQUIREMENTS:-requirements.txt}
RUN apk --purge del .build-deps

COPY . .

EXPOSE 8000
