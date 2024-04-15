FROM python:3.12

RUN mkdir -p /apifast

ENV PYTHONPATH='apifast'

WORKDIR apifast/
COPY req.txt .

RUN ls

RUN pip install -r req.txt

WORKDIR /
CMD ["python", "-m", "apifast.run"]