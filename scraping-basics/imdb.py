from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


class Movie:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.imdb_rating = kwargs.get('imdb_rating')
        self.description = kwargs.get('description')

    def output_dict(self):
        """
        Return a dictionary representation of this Movie object
        """
        return {
            'title': self.title,
            'imdb_rating': self.imdb_rating,
            'description': self.description,
        }


class IMDBScraper:
    def __init__(self, start_url, params=None):
        self.start_url = start_url
        self.params = params
        self.soup = None
        self.output = []

    def extract_movies(self):
        """
        Extract the list of movies from the page retrieved from start_url
        """
        content = self.request_page(self.start_url)
        self.soup = BeautifulSoup(content, features='html.parser')
        list_items = self.soup.select('.lister-list tr')

        for item in list_items:
            movie = Movie()

            # Scrape title and rating from parent page
            title_element = item.select_one('.titleColumn')
            movie.title = title_element.text
            movie.imdb_rating = item.select_one('.imdbRating').text

            # Scrape description from details page
            details_url = title_element.select_one('a').get('href')
            details_url = urljoin(self.start_url, details_url)
            details = self.extract_movie_details(details_url)
            movie.description = details['description']
            
            # Add the movie to the output list
            self.output.append(movie.output_dict())

    def request_page(self, url, params=None):
        """
        Retrieve the raw HTML from a url
        """
        result = requests.get(url, params=params)
        if not result.ok:
            raise Exception(f'Could not retrieve page from {url}')
        return result.content

    def extract_movie_details(self, details_url):
        """
        Extract additional information from a child page
        """
        content = self.request_page(details_url)
        self.soup = BeautifulSoup(content, features='html.parser')
        description = (self.soup
                            .select_one('.GenresAndPlot__ContentParent-cum89p-8 p')
                            .select_one('span:nth-of-type(1)')
                            .text
                      )

        return {
            'description': description,
        }

    def save_output_to_mongo(self):
        """
        Optional function: implement this function if you want to save the
        scraped output to your MongoDB.
        """
        pass


if __name__ == '__main__':
    imdb_url = 'https://www.imdb.com/chart/top/'
    params = {'ref_': 'nv_mv_250'}
    scraper = IMDBScraper(imdb_url, params=params)
    
    scraper.extract_movies()
    # To get the movie list output, comment out the following:
    # output = scraper.output

    # Comment out below if you don't want to save the output to MongoDB
    # scraper.save_output_to_mongo()