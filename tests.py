import unittest
from web_scrapper import WebScrapperService, clean


class Test(unittest.TestCase):
    """
    Test data is arranged in a list of tuples: (item number, test attribute, expected value)
    NOTE: if following the website some data on "genre and release date" attributes is hidden
    """

    url = 'https://silverbirdcinemas.com/cinema/accra/'
    # fixture has to be changed according to the current website content
    data = [
        (1, "showtime", "FRI - SUN:  12:10PM, 2:00PM, 3:50PM, 5:40PM, 7:30PM, 9:30PM"),
        (1, "genre", "Action, Adventure, Comedy, Now Showing"),
        (2, "title", "A SIMPLE FAVOR"),
        (4, "duration", "02 hours 01 minutes"),
        (5, "title", "THE NUN"),
        (5, "release_date", "Sep 07, 2018"),
        (8, "title", "THE MEG"),
    ]

    def test_web_scrapper(self):
        result = WebScrapperService.get_html(self.url)
        # print(result)

        # first test checks if the returned number of movies is nine
        self.assertEqual(len(result), 10)

        for n, attr, expected in self.data:
            # testing each tuple case in the Test data
            self.assertEqual(result[n-1].__getattribute__(attr).lower(), clean(expected.lower()))


if __name__ == "__main__":
    unittest.main()