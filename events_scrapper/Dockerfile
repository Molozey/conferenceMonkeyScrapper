FROM python:3.12

RUN mkdir -p /events_scrapper

ENV PYTHONPATH='events_scrapper'

WORKDIR events_scrapper/
COPY req.txt .

RUN ls

RUN pip install -r req.txt

WORKDIR /
CMD ["python", "-m", "events_scrapper.serve"]