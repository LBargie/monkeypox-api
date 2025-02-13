# Monkeypox API 

This API can be used to fetch the UK's Monkeypox infection case numbers for analysis.

Under the hood I am using the BeautifulSoup package to scrape the case numbers from the UK government website:

https://www.gov.uk/government/publications/monkeypox-outbreak-epidemiological-overview/

Run the API by entering `uv run uvicorn src.api.main:app --port 8000` on your command prompt/terminal.

Check out the documentation for help:

https://fastapi.tiangolo.com

https://beautiful-soup-4.readthedocs.io/en/latest/

https://www.uvicorn.org
