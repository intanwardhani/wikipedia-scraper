# UTF-8 Python 3.13.5
# Utility functions for leaders-related classes
# Author: Intan K. Wardhani

import requests, time, random

class Leader:
    
    """A class representing API data.
    
    """
    
    def __init__(self) -> None:
        self.root_url = "https://country-leaders.onrender.com"
        self.status_url = "https://country-leaders.onrender.com/status/"
        
    def check_status(self) -> None:
        self.req_status = requests.get(self.status_url, timeout=5)
        if self.req_status == 200:
            print(self.req_status.text)
        else:
            print(self.req_status.status_code)
    
    def get_leaders(self) -> tuple:
    
        """A function to extract leaders from different countries."""
        
        timeout = time.sleep(random.uniform(5.0, 7.0))
        
        # define urls
        countries_url = "https://country-leaders.onrender.com/countries/"
        cookie_url = "https://country-leaders.onrender.com/cookie/"
        leaders_url = "https://country-leaders.onrender.com/leaders"
        
        # set polite user-agent
        headers = {
                    "User-Agent": f"wikipedia-scraper/0.1 (+https://country-leaders.onrender.com)"
                }
        session = requests.Session()
        session.headers.update(headers)
        
        # get the cookies
        cookies = session.get(cookie_url, timeout=timeout)
        
        # get the countries
        countries = session.get(countries_url, timeout=timeout).json()
        
        # loop over countries and save the leaders in a dict
        leaders_per_country = {
                                country: session.get(
                                    leaders_url, 
                                    cookies=cookies.cookies, 
                                    timeout=timeout, 
                                    params={'country': country}
                                    ).json()
                                for country in countries
                            }
        
        # loop over leaders to get the wiki url from each leader
        req_url_list = []
        for country_code, leaders_list in leaders_per_country.items():
            for i in range(len(leaders_list)):
                leader = leaders_per_country[country_code][i]
                req_leader = session.get(leader['wikipedia_url'], timeout=timeout)
                req_url_list.append(req_leader)
                
        # return the leaders dict and url list
        return leaders_per_country, req_url_list

