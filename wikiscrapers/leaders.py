# UTF-8 Python 3.13.5
# Utility functions for leaders-related classes
# Author: Intan K. Wardhani

import requests
import time
import random

class Leader:
        
    """
    A class representing API data to extract leaders from different countries and their Wikipedia pages.

    This class uses the `country-leaders.onrender.com` API to retrieve a list of countries, 
    fetch leaders for each country, and obtain the raw Wikipedia pages for each leader. 
    It also includes a private method for checking the API status.

    Attributes
    ----------
    root_url : str
        Base URL for the API.
    status_url : str
        URL for checking the API status.
    session : requests.Session
        A requests Session object with a preset User-Agent header for polite scraping.

    Methods
    -------
    _check_status()
        Private method to check the API status before making other requests. 
        Prints the status or any request exceptions.
    get_leaders() -> tuple
        Retrieves leaders per country and their Wikipedia pages.
        Returns:
            tuple: 
                - dict mapping country names to lists of leaders
                - list of requests.Response objects for each leader's Wikipedia page
    """

    def __init__(self) -> None:
        self.root_url = "https://country-leaders.onrender.com"
        self.status_url = f"{self.root_url}/status/"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"wikipedia-scraper/0.1 (+{self.root_url})"
        })

    def _check_status(self) -> None:
        """Private method to check API status."""
        try:
            response = self.session.get(self.status_url, timeout=5)
            response.raise_for_status()
            print(response.text)
        except requests.RequestException as e:
            print(f"Status check failed: {e}")

    def get_leaders(self) -> tuple:
        """Retrieve leaders from all countries and their Wikipedia pages."""

        # Polite delay range (seconds)
        delay_min, delay_max = 2.0, 5.0

        # Check API status before proceeding
        self._check_status()

        # Define API endpoints
        countries_url = f"{self.root_url}/countries/"
        cookie_url = f"{self.root_url}/cookie/"
        leaders_url = f"{self.root_url}/leaders"

        # Get cookies and countries
        cookies = self.session.get(cookie_url, timeout=5)
        countries = self.session.get(countries_url, cookies=cookies.cookies, timeout=5).json()

        # Fetch leaders per country
        leaders_per_country = {}
        for country in countries:
            response = self.session.get(
                leaders_url,
                cookies=cookies.cookies,
                timeout=5,
                params={"country": country},
            )
            leaders_per_country[country] = response.json()

        # Fetch Wikipedia pages for each leader
        req_url_list = []
        for _, leaders_list in leaders_per_country.items():
            for leader in leaders_list:
                time.sleep(random.uniform(delay_min, delay_max))  # polite delay
                resp = self.session.get(leader["wikipedia_url"], timeout=5)
                req_url_list.append(resp)

        # Return the results
        return leaders_per_country, req_url_list


