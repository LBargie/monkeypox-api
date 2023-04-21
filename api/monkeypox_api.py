from typing import List, Optional, Type
from fastapi import FastAPI, Query, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, BaseConfig, Field
from .scraper.scrape import MonkeypoxScraper
import re

# create MonkeypoxScraper object
scraper = MonkeypoxScraper()

# function for checking the date format
def date_checker(date: str) -> HTTPException:

    if not re.fullmatch("\d{4}-\d{2}-\d{2}", date):
        raise HTTPException(status_code=422, detail="Search date must be in the format YYYY-MM-DD")

# function for checking the date format in range endpoint
def range_checker(start_date: str, end_date: str) -> HTTPException:

    if not (re.fullmatch("\d{4}-\d{2}-\d{2}", start_date) and re.fullmatch("\d{4}-\d{2}-\d{2}", end_date)):
        raise HTTPException(status_code=422, detail="Search date must be in the format YYYY-MM-DD")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the UK monkeypox data API"}

@app.get("/info")
async def available_data():

    available_data = scraper.available_data()

    for k, v in available_data.items():
        available_data.update({k: "https://www.gov.uk" + v})

    return available_data

@app.get("/latestdata/")
async def latest_data():

    data = scraper.available_data()

    date = list(data.keys())[len(data.keys())-1]

    return scraper.search_by_date(date=date)

@app.get("/search_by_date/{date}", dependencies=[Depends(date_checker)])
async def search_by_date(date: str):

    return scraper.search_by_date(date=date)

@app.get("/search_range/{start_date}/{end_date}", dependencies=[Depends(range_checker)])
async def search_range(start_date: str, end_date: str):

    dates = [start_date, end_date]

    return scraper.search_date_range(date_range=dates)

@app.get("/alldata")
async def search_all_dates():

    return scraper.search_all_dates()
