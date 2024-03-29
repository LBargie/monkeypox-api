# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./api /code/api

# 
CMD ["uvicorn", "api.monkeypox_api:app", "--host", "0.0.0.0", "--port", "80"]