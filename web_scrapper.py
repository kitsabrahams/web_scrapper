"""
Web Scrapper to extract all the cinema data from a website
https://silverbirdcinemas.com/cinema/accra/
:author Ibrahim Kitagenda <ibrahim.kitagenda@gmail.com>
"""
import re
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


class WebScrapperService:
    @staticmethod
    def get_html(url):
        """
        Checks if the website is available, parses the returned html with
        BeautifulSoup, extracts the movie container div and processes it
        :param url: Takes the website url
        :return: list of Movie objects
        """
        try:
            response = get(url)
        except RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        movies = []
        for item in soup.select('div#cinema-m div.entry-content'):
            movie = Movie(item)
            movies.append(movie)
        return movies


class Movie:
    title = release_date = duration = genre = language = showtime = '--'

    def __init__(self, item=None):
        if item:
            self.item = item
            self.set_fields()

    def set_fields(self):
        # title and duration are on the same html tree level
        # all value strings are cleaned before assignment
        try:
            self.title = clean((self.item.find('a')).text)
            self.duration = clean((self.item.find('div', attrs={'class': 'entry-date'})).text)
            # showtime is on the same tree but it's divided into two
            self.set_showtime()
            # genre if on one level deeper and has values <a> tags
            self.set_genre()
            # release_date and language are on the same level as genre but have not identifiers so
            # they can only be extracted using their div positions
            self.set_release_date()
            self.set_language()
        except Exception as e:
            print('This Item has an Error: {}'.format(str(e)))

    def set_genre(self):
        note = self.item.find('div', attrs={'class': 'note'})
        genres = []
        for genre in note.findAll('a'):
            genres.append(clean(genre.text))
        self.genre = ", ".join(genres)

    def set_showtime(self):
        scope = self.item.find('p', attrs={'class': 'cinema_page_showtime'})
        days = (scope.find('span')).text
        time = (scope.select('strong')[1]).text
        self.showtime = clean(days + time)

    def set_language(self):
        scope = self.item.find('div', attrs='desc-mv')
        language = (scope.findAll('div'))[2].text
        self.language = clean(language.replace('Language:', ''))

    def set_release_date(self):
        scope = self.item.find('div', attrs='desc-mv')
        release = (scope.findAll('div'))[0].text
        self.release_date = clean(release.replace('Release:', ''))

    def __repr__(self):
        return repr({"title": self.title, "release_date": self.release_date,
                     "duration": self.duration, "showtime": self.showtime,
                     "genre": self.genre, "language": self.language})


def clean(string):
    """
    Helper function for replacing multi-spaces with a single space,
    removes leading and trailing spaces
    :param string:
    :return: 
    """
    return re.sub(' +', ' ', string.strip())
