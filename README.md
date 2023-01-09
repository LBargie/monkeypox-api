# Monkeypox API 

This API can be used to fetch the UK's Monkeypox infection case numbers for analysis.

The API was build using FastAPI and the BeautifulSoup package was used to scrape the case numbers from the UK government website:

https://www.gov.uk/government/publications/monkeypox-outbreak-epidemiological-overview/

FastAPI, BeautifulSoup and Uvicorn need to be installed to use the API. These can be pip installed.

To run the API, run: 

uvicorn monkeypox_api:app 

on your command prompt/terminal.

I have included a Jupyter Notebook with an example of how to get data from the API and analyse the results. 

Check out the documentation for help:

https://fastapi.tiangolo.com

https://beautiful-soup-4.readthedocs.io/en/latest/

https://www.uvicorn.org

Hope you find it useful and reach out with any questions. I build this API mostly for sharpening my skills. I hadn't build an API before so I wanted to try out the FastAPI and BeautifulSoup packages.
