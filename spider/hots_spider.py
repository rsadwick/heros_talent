import urllib2
from bs4 import BeautifulSoup, NavigableString, Tag

class HeroSpider(object):

    def __init__(self):
        self.base_url = "http://www.heroesfire.com/ajax/tooltip?relation_type=WikibaseArticle&relation_id="
        self.get_content()

    def scrape(self, curse_id):
        request = urllib2.Request(self.base_url + curse_id, headers={'User-Agent': 'Mozilla/5.0'})

        try:
            print curse_id
            html = urllib2.urlopen(request).read()
            soup = BeautifulSoup(html)
            return soup
        except urllib2.HTTPError, e:
            print ("some error with this id: " + curse_id)

    def get_content(self):

        for cnt in xrange(800):
            soup = self.scrape(str(cnt))
            #soup = self.scrape('64')
            if soup is not None:
                #figure out what kind of data this is: hero, talent, ability
                #checks on this image that keys off if markup is hero or talent
                image = soup.find_all("img")
                if image:
                    for source in image:
                        #figure out if this is a hero
                        path = source.get("src")
                        parts = path.split("/")
                        if path.split("/")[2] == 'hero':
                            self.parse_hero(soup)
                        elif len(parts) > 4 and path.split("/")[4] == 'talents':
                            self.parse_talents(soup)
                        elif len(parts) > 4 and path.split("/")[4] == 'abilities':
                            self.parse_ability(soup)

    def parse_hero(self, markup):
        print "hero markup"
        name = markup.find("h3").text
        print name

    def parse_talents(self, markup):
        print "talent markup"
        name = markup.find("h5").text
        for br in markup.find_all("h5"):
            print br.parent.get_text()

    def parse_ability(self, markup):
        print "ability markup"
        name = markup.find("h5").text
        for br in markup.find_all("h5"):
            print br.parent.get_text()