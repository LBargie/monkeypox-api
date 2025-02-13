from typing import List
from bs4 import BeautifulSoup
import httpx
import re
from datetime import datetime
from pydantic import BaseModel, RootModel


MPOX_URL = "https://www.gov.uk/government/publications/monkeypox-outbreak-epidemiological-overview"


class Report(BaseModel):
    date: str
    url: str

Reports = RootModel[List[Report]]


def overview_links(url: str, search_string: str) -> List[str]:

    response = httpx.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all(href=re.compile(search_string))
    
    return [link.get("href") for link in links]


def extract_report_dates(url: str) -> datetime:
    """
        Extract the date from a URL containing the monkeypox data.
        
        Arguments:
            url: the monkeypox URL containing the date to be extracted.

        Returns:
            datetime object representing the date extracted from the URL.
        
    """

    dates = re.findall("\d+-\w+-\d{4}", url)

    return datetime.strptime(dates[0], "%d-%B-%Y").date()


def available_reports() -> Reports:
    response = sorted(
        set(overview_links(url=MPOX_URL, search_string="mpox-outbreak-epidemiological-overview-")), 
        reverse=True, 
        key=extract_report_dates
        )
    dates = sorted(set([extract_report_dates(url).isoformat() for url in response]), reverse=True)
    reports = [Report(url=url, date=date) for url, date in zip(response, dates)]
    return Reports(reports)
