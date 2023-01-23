# Monkeypox API 

This API can be used to fetch the UK's Monkeypox infection case numbers for analysis.

Under the hood I am using the BeautifulSoup package to scrape the case numbers from the UK government website:

https://www.gov.uk/government/publications/monkeypox-outbreak-epidemiological-overview/

FastAPI, BeautifulSoup and Uvicorn need to be installed to use the API. These can be pip installed:

```
pip install fastapi

pip install beautifulsoup4
```

Run the API by entering `uvicorn monkeypox_api:app` on your command prompt/terminal.

I have included a Jupyter Notebook with an example of how to get data from the API and analyse the results. 

Check out the documentation for help:

https://fastapi.tiangolo.com

https://beautiful-soup-4.readthedocs.io/en/latest/

https://www.uvicorn.org

### Docker Container

To build the image run the following on the command line (in the same directory as the Dockerfile):

`docker build -t monkeypox-api .`

Alternatively, pull the image from my Docker Hub repository using the following on the command line:

`docker pull lbargie/monkeypox-api`

To run the app enter the following on the command line:

docker run --rm -p 80:80 monkeypox-api

Navigate to http://localhost:8080 in your web browser to view the app.

Hope you find it useful and reach out with any questions. I build this API mostly for sharpening my skills. I hadn't build an API before so I wanted to try out the FastAPI and BeautifulSoup packages.

