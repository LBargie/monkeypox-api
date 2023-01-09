from typing import List
from fastapi import FastAPI, Query, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from scraper.scrape import MonkeypoxScraper


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"error": "Search date must be in the format YYYY-MM-DD"}),
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the UK monkeypox data API"}

@app.get("/info")
async def available_data(scraper: MonkeypoxScraper = Depends(MonkeypoxScraper)):
    
    available_data = scraper.available_data()

    for k, v in available_data.items():
        available_data.update({k: "https://www.gov.uk" + v})

    return available_data

@app.get("/latestdata/")
async def latest_data(scraper: MonkeypoxScraper = Depends(MonkeypoxScraper)):

    data = scraper.available_data()

    date = list(data.keys())[len(data.keys())-1]

    return scraper.search_by_date(date=date)

@app.get("/search_by_date/")
async def search_by_date(
    search_date: str = Query(regex="\d{4}-\d{2}-\d{2}"), 
    scraper: MonkeypoxScraper= Depends(MonkeypoxScraper)
    ):

    return scraper.search_by_date(date=search_date)

@app.get("/search_multiple/")
async def search_multiple(
    search_dates: List[str] = Query(regex="\d{4}-\d{2}-\d{2}"),
    scraper: MonkeypoxScraper= Depends(MonkeypoxScraper)
    ):

    return scraper.search_multiple_dates(dates=search_dates)

@app.get("/search_range/")
async def search_range(
    start_date: str = Query(regex="\d{4}-\d{2}-\d{2}"), 
    end_date: str = Query(regex="\d{4}-\d{2}-\d{2}"),
    scraper: MonkeypoxScraper = Depends(MonkeypoxScraper)
    ):

    dates = [start_date, end_date]

    return scraper.search_date_range(date_range=dates)

@app.get("/alldata")
async def search_all_dates(scraper: MonkeypoxScraper=Depends(MonkeypoxScraper)):

    return scraper.search_all_dates()
