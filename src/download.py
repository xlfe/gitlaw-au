
import json
import time
from lxml import html
import requests

#https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()

link_start = 'ctl00_MainContent_AttachmentsRepeater'
link_end = 'hlPrimaryDoc'

class Legislation(object):

    def __init__(self, comlaw_id):
        self.cli = comlaw_id

    def download_links(self):

        download_pg = 'http://www.comlaw.gov.au/Details/{}/Download'.format(self.cli)
        r = requests.get(download_pg, verify=False)

        if r.status_code != 200:
            raise Exception('Error loading details page for {}'.format(self.cli))

        h = html.fromstring(r.content)

        status = h.xpath('//*[@id="ctl00_MainContent_ucItemPane_lblStatus"]')[0].text_content()
        title = h.xpath('//*[@id="ctl00_MainContent_ucItemPane_lblTitleGeneric"]')[0].text_content()

        volumes = []
        links = []
        pages = []

        for n in h.xpath('//*[@class="LegSubTitle"]'):
            if 'id' in n.attrib and n.attrib['id'].endswith('_ArtifactName'):

                sub_name = n.text_content()
                div = n.getnext().getnext()

                for a in div.xpath('.//a'):
                    if 'id' in a.attrib and a.attrib['id'].startswith(link_start) and a.attrib['id'].endswith(link_end):

                        imgs = a.findall('img')

                        if len(imgs) != 1:
                            continue

                        url = imgs[0].attrib['src'].split('/')[-1]
                        url = url.split('.')[0]

                        links.append((url, a.attrib['href'], sub_name))

                for r in div.xpath('.//span[@class="RedText"]'):

                    if 'id' not in r.attrib:
                        continue

                    tc = r.text_content().strip()
                    if r.attrib['id'].endswith('lblMyVolNum'):
                        volumes.append(tc)
                    elif r.attrib['id'].endswith('lblMyPageNum'):
                        pages.append(tc)


        assert len(pages) == len(volumes), '{} had mismatch - pages: {} volumes:{} links{}'.format(self.cli, len(pages), len(volumes),len(links))
        assert len(links) == len(volumes), '{} had mismatch - pages: {} volumes:{} links{}'.format(self.cli, len(pages), len(volumes),len(links))
        return [{
                    'ComLawID': self.cli,
                    'title': title,
                    'status':status,
                    'type': l[0],
                    'url': l[1],
                    'subname': l[2],
                    'volname': v,
                    'pages': p
                } for l,v,p in zip(links, volumes,pages)]



#Don't need to use this - checkout details_current.json in this repo
#And you can download the files referenced in details_current.json
#   from https://s3.amazonaws.com/gitlaw-au/gitlaw-au-current-2015-07-05.tar.gz


INPUT = './acts_current.txt'

with open(INPUT,'r') as inp:

    for line in inp:
        if not line.startswith('('):
            continue

        #Be nice again
        time.sleep(3)

        name,cli = line.split(", '")
        name = name[2:-1]
        cli = cli[:-3]

        d = Legislation(cli)
        print '#downloading links for {} {}'.format(cli, name)
        try:
            for l in d.download_links():
                print json.dumps(l, indent=1)
        except Exception as e:
            print '# Unable to download {}: {}'.format(cli, e.message)

