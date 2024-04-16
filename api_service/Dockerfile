FROM python:3.12

RUN mkdir -p /api_service

ENV PYTHONPATH='api_service'

WORKDIR api_service/
COPY req.txt .

RUN ls

RUN pip install -r req.txt

WORKDIR /
CMD ["python", "-m", "api_service.run"]