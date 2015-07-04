
from lxml import html
import requests
from docx import Document
import StringIO

link_xtree = '//*[@id="ctl00_MainContent_AttachmentsRepeater_ctl00_ArtifactVersionRenderer_Repeater1_ctl00_ArtifactFormatTableRenderer1_RadGridNonHtml_ctl00_ctl04_hlPrimaryDoc"]'

SPIDER_DELAY=10000


class Legislation(object):

    def __init__(self, comlaw_id):
        self.cli = comlaw_id

        self.docx = self.download_legislation_document()

    def download_legislation_document(self):

        download_pg = 'http://www.comlaw.gov.au/Details/{}/Download'.format(self.cli)
        r = requests.get(download_pg, verify=False)

        if r.status_code != 200:
            raise Exception("Couldn't download file")

        h = html.fromstring(r.content)

        a = h.xpath(link_xtree)[0]

        d = requests.get(a.attrib['href'], verify = False)
        s = StringIO.StringIO(d.content)

        return Document(s)

    def text(self):

        for p in self.docx.paragraphs:
            print p.text






