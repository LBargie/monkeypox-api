from typing import Dict, List, Union
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
from datetime import datetime


class MonkeypoxScraper:
    mainurl = "https://www.gov.uk/government/publications/monkeypox-outbreak-epidemiological-overview#full-publication-update-history"
    nations = ["England", "Northern Ireland", "Scotland", "Wales", "Total"] 

    def __init__(self):

        self.urls = list(set(self.get_main_links(self.mainurl)))

        self.urls.sort(key=lambda x: self.extract_dates(x))

        self.dates = [self.extract_dates(url).isoformat() for url in list(set(self.urls))]

        self.dates.sort()

    def url_response(self, url: str) -> None:

        return urlopen(url).read().decode("utf-8")

    def beaut_soup(self, url_response) -> None:
        
        return BeautifulSoup(url_response, "html.parser")

    def get_main_links(self, mainurl: str) -> List[str]:

        response = self.url_response(mainurl)

        soup = self.beaut_soup(response)

        links = soup.find_all(href=re.compile("monkeypox-outbreak-epidemiological-overview-"))  
        
        return [link.get("href") for link in links]

    def extract_dates(self, url: str) -> datetime:
        """
        Extract the date from a URL containing the monkeypox data.
        
        Arguments:
            url: the monkeypox URL containing the date to be extracted.

        Returns:
            datetime object representing the date extracted from the URL.
        
        """

        dates = re.findall("\d+-\w+-\d{4}", url)

        return datetime.strptime(dates[0], "%d-%B-%Y").date()

    def available_data(self) -> Dict[str, str]:

        return {k: v for k, v in zip([date for date in self.dates], self.urls)}

    def search_by_date(self, date: str) -> Dict[str, str]:

        try:
            
            requested_data = self.available_data()[date]
        
        except KeyError:
            
            return {"date": date, "records": "no records exist for specified date"}
        
        else:

            response = self.url_response(f"https://www.gov.uk/{requested_data}")

            soup = self.beaut_soup(response)

            rows = soup.find_all("td")
            # headers = soup.find_all("th")

            data = []

            for row in rows:

                results = row.text.replace(",", "")

                results2 = re.findall("\d+", results)

                data.append(int(results2[0])) if len(results2) != 0 else None

            if date <= "2022-06-21":
                results = [[v] for v in data[:5]]
                headers = ["UK Nation", "Confirmed"]

            elif date > "2022-06-21" and date <= "2022-07-22":
                results = [data[:10][i:i+2] for i in range(0, len(data[:10]), 2)]
                headers = ["UK Nation", "Confirmed", "Change Since Last Report"]

            else: 
                results = [data[:15][i:i+3] for i in range(0, len(data[:15]), 3)]
                headers = ["UK Nation", "Total", "Confirmed", "Highly Probable"]
                
            for result, nation in zip(results, self.nations):
                result.insert(0, nation)
            
            ls = []

            for res in results:
                d = {}
                for i, v in zip(headers, res):
                    d[i] = v
                ls.append(d)

            return {"date": date, "records": ls}

    def search_list(self, date_list: List[str]) -> Dict[str, str]:

        records = []

        for date in date_list:
            data = self.search_by_date(date=date)
            records.append(data)

        return {i: v for i, v in enumerate(records)}
    
    def search_multiple_dates(self, dates: List[str]) -> Dict[str, str]:

        return self.search_list(dates)

    def search_date_range(self, date_range: List[str]) -> Dict[str, str]:

        if len(date_range) != 2:
            raise ValueError("date_range argument must be a list of length 2")
        else:
            dates_in_range = [i for i, v in enumerate(self.dates) if v in date_range]
            dates = self.dates[dates_in_range[0]: dates_in_range[-1]+1]

            return self.search_list(dates)

    def search_all_dates(self) -> Dict[str, str]:

        return self.search_list(self.dates)
