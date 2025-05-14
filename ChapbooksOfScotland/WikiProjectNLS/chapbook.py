class Chapbook(object):

    def __init__(self, wikisource_url, series, title, subtitle=None, pages=None):
        self.wikisource_url = wikisource_url
        self.series = series
        self.title = title
        self.subtitle = subtitle
        self.pages = pages

    def set_pages(self, pages):
        self.pages = pages

    def __str__(self):
        return {
            "wikisource_url": self.wikisource_url,
            "series": self.series,
            "title": self.title,
            "subtitle": self.subtitle
        }.__str__()

