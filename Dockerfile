# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./api /code/api

COPY ./api/scraper /code/api/scraper

# 
CMD ["uvicorn", "api.monkeypox_api:app", "--host", "0.0.0.0", "--port", "80"]