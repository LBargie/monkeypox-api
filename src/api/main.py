from typing import Annotated, Any
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import RootModel, BaseModel, Field
from src.scraper.main import available_reports, Reports
import pandas as pd


DateRequest = Annotated[
    str,
    Field(
        description="The date to search for in the format YYYY-MM-DD",
        pattern="\d{4}-\d{2}-\d{2}",
    ),
]

Record = list[dict[str, Any]]


class Records(BaseModel):
    date: str
    records: dict[int, Record]


RecordsResponse = RootModel[list[Records]]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the UK monkeypox data API"}


@app.get("/data", description="The available reports")
async def available_data() -> Reports:
    return available_reports()


@app.get("/data/latest")
async def latest_data() -> Records:
    reports = available_reports()

    date = reports.root[0].date

    dfs = pd.read_html(f"https://www.gov.uk/{reports.root[0].url}", flavor="bs4")

    return Records(
        date=date, records={k: v.to_dict(orient="records") for k, v in enumerate(dfs)}
    )


@app.get("/data/{date}")
async def search_by_date(date: DateRequest) -> Records:
    reports = available_reports()
    report = next((report for report in reports.root if report.date == date), None)

    if report:
        dfs = pd.read_html(f"https://www.gov.uk/{report.url}", flavor="bs4")
        return Records(
            date=report.date,
            records={k: v.to_dict(orient="records") for k, v in enumerate(dfs)},
        )
    else:
        raise HTTPException(
            status_code=404, detail="No records exist for specified date"
        )


@app.get("/data/{start_date}/{end_date}")
async def search_range(
    start_date: DateRequest, end_date: DateRequest
) -> RecordsResponse:
    data = available_reports()

    responses = []
    for report in data.root:
        if report.date >= start_date and report.date <= end_date:
            dfs = pd.read_html(f"https://www.gov.uk/{report.url}", flavor="bs4")
            records = {k: v.to_dict(orient="records") for k, v in enumerate(dfs)}
            responses.append(Records(date=report.date, records=records))

    return responses
