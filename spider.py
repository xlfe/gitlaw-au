#
# This file will crawl ComLaw and download the name and ComLawID of all legislation
# Starting in 2015 and working backwards to 1901
#
# For example - use like:
#  python -u spider.py > legislation.txt
#
# You don't actually need to run this - I have included both the current legislative instruments
# and asmade in the repo:
# acts_current.txt
# acts_asmade.txt



import mechanize
import time


# AspNET *SIGH*
FORM_NAME = 'aspnetForm'

#Current Acts only...
BASE_CURRENT = 'https://www.comlaw.gov.au/Browse/Results/ByYearNumber/Acts/Current/{}/0'

#As made
BASE_ASMADE = 'https://www.comlaw.gov.au/Browse/Results/ByYearNumber/Acts/Asmade/{}/0'



class ComlawYear(object):

    def __init__(self, year, BASE=BASE_CURRENT):
        self.y = year
        self.br = mechanize.Browser()
        self.br.open(BASE.format(self.y))

        print 'Opened first page of year {}'.format(year)
        self.pages = 1

    def get_page(self):


        links = []

        for l in self.br.links():
            #Only get the links to legislation "LegBookmarks"
            if ('class', 'LegBookmark') in l.attrs:

                #Save the name of the legislation and its ComlawID
                links.append((
                    l.text,
                    l.url.split('/')[-1]
                ))

        return links


    def next_page(self):

        # control = self.br.form.find_control(NEXT_PG_CONTROL)
        self.br.select_form(FORM_NAME)

        for c in self.br.form.controls:
            if 'class' in c.attrs and c.attrs['class'] == 'rgPageNext':

                #We've come to the end of the pages...
                if 'onclick' in c.attrs and c.attrs['onclick'].startswith('return'):
                    return False
                self.br.submit(c.name)
                self.pages += 1
                return True

        return False

    def get_all(self):

        while True:

            for l in self.get_page():
                yield l

            #be nice to the web server!
            time.sleep(2)

            if self.next_page() is False:
                print 'Year {} had {} pages'.format(self.y, self.pages)
                return



#Don't need to use this - checkout acts_asmade.txt and acts_current.txt in the repo!
if False:
    year = 2015

    while True:

        y = ComlawYear(year)
        for l in y.get_all():
            print l
        year -= 1

        if year < 1901:
            break

    print 'Done'


