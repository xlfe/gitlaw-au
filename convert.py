
# Convert the downloaded documents to markdown and put them in the right folder

INPUT = './details_current.json'


import collections
import subprocess
import os
import json

from docx import Document
from docx.shared import Pt



class TextUtil(object):

    PANDOC_OPTIONS = 'pandoc -f docx -t markdown_github --no-wrap --ascii '
    def check_dir(self, dir):

        if not os.path.exists(dir):
            os.makedirs(dir)

    def convert(self, input, output, type):

        # if type == 'iconDOCX':
        #     return
        #print 'Converting {} {} -> {}.md'.format(type, input, output)


        if type == 'iconDOCX':
            docx = Document(input)
        else:
            command = 'textutil -convert docx -stdout ./{} >| ./tmp'.format(input)
            subprocess.check_call(command, shell=True)
            docx = Document('./tmp')
            os.remove('./tmp')


        normal = docx.styles['Normal']

        if docx.styles['Normal'] and docx.styles['Normal'].font and docx.styles['Normal'].font.size:
            normal_size = docx.styles['Normal'].font.size.pt
        else:
            normal_size = Pt(11).pt


        indents = collections.defaultdict(int)
        font_sizes = collections.defaultdict(int)
        prev_indent = 0

        for p in docx.paragraphs:
            if len(p.text.strip()) == 0:
                continue

            indent = p.paragraph_format.left_indent / 635 if p.paragraph_format.left_indent is not None else 0
            indents[indent] += 1

            if p.style.font and p.style.font.size:
                p_size = p.style.font.size.pt
            elif p.style.base_style and p.style.base_style.font and p.style.base_style.font.size:
                p_size = p.style.base_style.font.size.pt
            else:
                p_size = normal_size

            for r in p.runs:

                r_size = r.font.size.pt if r.font.size is not None else p_size
                font_sizes[r_size] += 1


        font_sizes_ordered = sorted(font_sizes.iterkeys(), key=lambda k:int(k), reverse=True)
        font_sizes_usage = sorted(font_sizes.iteritems(), key=lambda k:k[1], reverse=True)

        most_popular = font_sizes_usage[0][0]

        fonts = ''

        for f in font_sizes:
            if f == normal_size:
                fonts += '_{}_'.format(f)
            else:
                fonts += ' {} '.format(f)



        print '{}, {:<5}, {:<5}, {},{},  {}'.format(
            input,
            font_sizes_ordered[0],
            font_sizes_ordered[-1],
            int(normal_size),
            int(most_popular),
            ', '.join(str(int(f)) for f in font_sizes))


            # for i in range(len(p.text)/80 + 1):
            #     line = p.text[i*80:(i+1)*80]
            #     print '\t{}{}'.format(' '*indent, line.encode('ascii','ignore'))


        # for name, count in font_sizes.iteritems():
        #     print '{} {}'.format(name, count)
        #
        #
        # for name, count in sorted(indents.iteritems(), key=lambda k:k[0]):
        #     print '{} {}'.format(name, count)
        #
        # print '---------\n\n'





with open(INPUT, 'r') as inp:

    details = json.load(inp)





converter = TextUtil()


import re
keepcharacters = (' ','.','-','(',')','/')
going = True

print 'Loaded {} documents'.format(len(details))

for doc in details:

    if doc['uuid'] != '30708aa0-35ca-4847-a995-28ef137da240' and going == True:
        continue

    going=False

    if doc['type'] not in ['iconDOC', 'iconDOCX', 'iconRTF']:
        print 'Unable to convert {} of type {}'.format(doc['title'], doc['type'])
        continue


    directory = os.path.join('acts',doc['status'].lower(), doc['title'][0].lower())
    filename = doc['title'].lower()
    fullpath = os.path.join(directory, filename)

    fullpath = "".join(c for c in fullpath if c.isalnum() or c in keepcharacters).rstrip()

    # {
    #     u'status': u'Current',
    #     u'uuid': u'2f8dc4ff-7d4d-4769-9886-e9d93845ba03',
    #     u'title': u'Excise Act 1901',
    #     u'ComLawID': u'C2015C00135',
    #     u'subname': u'Act Compilation',
    #     u'volname': u'',
    #     u'type': u'iconDOCX',
    #     u'pages': u''
    # }

    converter.check_dir(directory)
    converter.convert(input=os.path.join('comlaw',doc['uuid']), output=fullpath, type=doc['type'])

