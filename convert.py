
# Convert the downloaded documents to markdown and put them in the right folder

INPUT = './details_current.json'


import collections
import subprocess
import os
import json

from docx import Document
from docx.shared import Pt

import re

code_map = [
    ('\r', ''),     #Character return
    (u'\xa0', ' '),     #Non breaking space
    (u'\u2018', "'"),   #Left single quotation mark
    (u'\u2019', "'"),   #Right single quotation mark
    (u'\u2022', ' + '),   #Bullet
    (u'\u201c', '"'),   #Left double quotation mark
    (u'\u201d', '"'),   #Right double quotation mark
    (u'\u2013', ' '),   #
    (u'\u2014', '--'),   #Em dash
    (u'\u2026', ' '),   #horizontal elipsis
    (u'\u2011', '-')    #Non-breaking hyphen
]
STYLE = collections.namedtuple('STYLE', 'BOLD ITALIC')

TEXT = collections.namedtuple('TEXT', 'bold italic indent heading new_para text')

def whitespace_handler(match):
    o = ''
    for c in match.group(0):
        if c == ' ':
            o += ' '
        elif c == '\t':
            o += '    '

    if o != '':
        return o + ' * '
    return o


class StyleManager(object):

    def __init__(self):
        self.s = STYLE(False, False)

    def this_style(self, rs, text):

        out = ''

        ts = STYLE(rs.bold, rs.italic)

        if self.s != ts:
            #change in style

            out += self.close()

            if ts.BOLD:
                out += '**'

            if ts.ITALIC:
                out += '_'

        self.s = ts
        out += text

        return out


    def close(self):
        out = ''
        if self.s.ITALIC:
            out += '_'
        if self.s.BOLD:
            out += '**'
        return out



class TextUtil(object):

    PANDOC_OPTIONS = 'pandoc -f docx -t markdown_github --no-wrap --ascii '
    def check_dir(self, dir):

        if not os.path.exists(dir):
            os.makedirs(dir)

    def convert(self, input, output, type):


        if type == 'iconDOCX':
            print 'Opening {}'.format(input)
            docx = Document(input)
        else:
            print 'converting from {} {}'.format(type, input)
            command = 'textutil -convert docx -stdout ./{} >| ./tmp'.format(input)
            subprocess.check_call(command, shell=True)
            docx = Document('./tmp')
            # os.remove('./tmp')

        normal = docx.styles['Normal']

        if docx.styles['Normal'] and docx.styles['Normal'].font and docx.styles['Normal'].font.size:
            normal_size = docx.styles['Normal'].font.size.pt
        else:
            normal_size = Pt(11).pt


        indents = collections.defaultdict(int)
        font_sizes = collections.defaultdict(int)
        prev_indent = 0

        for p in docx.paragraphs:
            if not p.text.strip():
                continue

            indent = p.paragraph_format.left_indent.pt if p.paragraph_format.left_indent is not None else 0
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
        most_common_size = font_sizes_usage[0][0]
        idx_most_common = font_sizes_ordered.index(most_common_size)
        out = []

        for p in docx.paragraphs:

            if not p.text.strip():
                continue


            if p.style.font and p.style.font.size:
                p_size = p.style.font.size.pt
            elif p.style.base_style and p.style.base_style.font and p.style.base_style.font.size:
                p_size = p.style.base_style.font.size.pt
            else:
                p_size = normal_size

            _indent = p.paragraph_format.left_indent.pt if p.paragraph_format.left_indent is not None else 0

            if _indent > 0:
                indent = int(_indent / p_size)
            else:
                indent = 0

            sizes = collections.defaultdict(int)
            for r in p.runs:

                r_size = r.font.size.pt if r.font.size is not None else p_size

                size_index = font_sizes_ordered.index(r_size) + 1

                if size_index > 6 or size_index > idx_most_common:
                    size_index = 0
                sizes[size_index] += 1

            size_index = sorted(sizes.iteritems(), key=lambda k:k[1], reverse=True)[0][0]

            for r in p.runs:

                run_indent = 0

                text = r.text
                for frm, to in code_map:
                    text = text.replace(frm, to)


                # while had_nl and text.startswith(' ') or text.startswith('\t'):
                #     if text.startswith(' '):
                #         run_indent += 1
                #     elif text.startswith('\t'):
                #         run_indent += 4
                #     text = text[1:]

                remove = r'(DOCPROPERTY ([a-zA-Z]+)|TOC \\o|PAGEREF _[a-zA-Z0-9]+ \\h [\d]+|STYLEREF [a-zA-Z0-9]+)'


                text = re.sub(remove,'',text)

                if text.replace(' ','') != '':
                    out.append(TEXT(
                        1 if r.bold == True else 0,
                        1 if r.italic == True else 0,
                        indent + run_indent,
                        size_index,
                        0,
                        text
                    ))

                # if not text.endswith('\n'):
                #     had_nl = False




            #Paragraph
            out.append(TEXT(0, 0, 0, 0, 1, None))

            # run += style.close()
            #
            # for line in run.split('\n'):
            #
            #
            #line = re.sub(r'^([\s]+)',whitespace_handler, line, count=1)
            #     out.append(heading + line)
            #     try:
            #         test = u'{}'.format(line.encode('ascii'))
            #     except:
            #         print line
            #         raise


        joined = []
        prev= {}
        buffer = ''

        for o in out:
            style = o._asdict().copy()
            text = style.pop('text')

            if style == prev:
                if text:
                    buffer += text
            else:
                if buffer != '':
                    prev['text'] = buffer
                    joined.append(TEXT(**prev))
                buffer = text
                prev = style



        return joined


def joined_to_md(joined):
    """
        Rules
                Bold and Italic are ignored in headings
                Headings are

    """


    for j in joined:
        if j.text:
            text = re.sub(r'^([\s]*)([a-z0-9\sA-Z]+:|\([0-9a-zA-Z\.]+\))([\s]*)', r'\1\3\2 ', j.text)
            #j.text = ''
            print j
            print '{}'.format(text)


    return ''
    return '\n'.join(str(s) for s in joined)
#




with open(INPUT, 'r') as inp:

    details = json.load(inp)



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



converter = TextUtil()


import re
keepcharacters = (' ','.','-','(',')','/')
WRITE = False

print 'Loaded {} documents'.format(len(details))

for doc in details:

    if int(doc['pages'].split(' ')[0]) > 20:
        continue

    directory = os.path.join('acts',doc['status'].lower(), doc['title'][0].lower())
    filename = doc['title'].lower() + '.md'
    fullpath = os.path.join(directory, filename)
    fullpath = "".join(c for c in fullpath if c.isalnum() or c in keepcharacters).rstrip()
    converter.check_dir(directory)

    if os.path.exists(fullpath):
        print 'already converted {}'.format(fullpath)
        continue

    if doc['type'] not in ['iconDOC', 'iconDOCX', 'iconRTF']:
        message = 'Unable to convert {} of type {}'.format(doc['title'], doc['type'])
        with open(fullpath, 'wb') as out:
            out.write(message)
        print message
        continue

    joined = converter.convert(input=os.path.join('comlaw',doc['uuid']), output=fullpath, type=doc['type'])
    result = joined_to_md(joined)
    if WRITE:
        print 'Converted {}'.format(fullpath)
        try:
            with open(fullpath, 'wb') as out:
                out.write(result)
        except:
            os.remove(fullpath)
            raise
    else:
        if result != '':
            print result




