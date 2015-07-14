
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
    (u'\u2011', '-')    #Non-breaking hyphen
]
STYLE = collections.namedtuple('STYLE', 'BOLD ITALIC')

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

        if type=='iconDOCX':
            return ''

        if type == 'iconDOCX':
            docx = Document(input)
        else:
            print 'converting from {}'.format(type)
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

        if len(indents) == 0:
            raise Exception()

        font_sizes_ordered = sorted(font_sizes.iterkeys(), key=lambda k:int(k), reverse=True)
        indent_levels_ordered = sorted(indents.iterkeys(), key=lambda k:int(k))
        font_sizes_usage = sorted(font_sizes.iteritems(), key=lambda k:k[1], reverse=True)
        most_common_size = font_sizes_usage[0][0]
        idx_most_common = font_sizes_ordered.index(most_common_size)
        prev_indent = 0
        indent = 0
        out = []

        for p in docx.paragraphs:

            if not p.text.strip():
                continue

            out.append('')

            _indent = p.paragraph_format.left_indent / 635 if p.paragraph_format.left_indent is not None else 0
            indent_idx = int(indent_levels_ordered.index(_indent))

            if _indent > 0:

                if indent_idx > prev_indent:
                    indent += 1
                elif indent_idx < prev_indent:
                    indent -= 1
            else:
                indent = 0

            if indent < 0:
                indent = 0


            prev_indent = indent_idx

            if p.style.font and p.style.font.size:
                p_size = p.style.font.size.pt
            elif p.style.base_style and p.style.base_style.font and p.style.base_style.font.size:
                p_size = p.style.base_style.font.size.pt
            else:
                p_size = normal_size

            if indent > 0:
                ind = ' ' * indent + '* '
            else:
                ind = ''

            sizes = collections.defaultdict(int)
            for r in p.runs:

                r_size = r.font.size.pt if r.font.size is not None else p_size

                size_index = font_sizes_ordered.index(r_size) + 1

                if size_index > 6 or size_index > idx_most_common:
                    size_index = 0
                sizes[size_index] += 1

            size_index = sorted(sizes.iteritems(), key=lambda k:k[1], reverse=True)[0][0]
            if size_index:
                heading = '#' * size_index
            else:
                heading = ''
            style = StyleManager()
            run = ''

            for r in p.runs:

                text = r.text
                for frm, to in code_map:
                    text = text.replace(frm, to)

                hasnl = '\n' in text

                for line in text.split('\n'):


                    #line = re.sub(r'^([\s]*)\(([0-9a-zA-Z\.]+)\)[\s]*',r'\1 * (\2) ', line, count=1)

                    run += ind + style.this_style(r,line)

                    if hasnl and heading != '':
                        raise Exception()
                    elif hasnl:
                        run += '\n'



            run += style.close()
            if heading == '' and (run.startswith(' ') or run.startswith('\t')):
                run = re.sub(r'^([\s]*)',r'\1 * ', run, count=1)

            out.append(heading + run)







        return '\n'.join(out)




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

    directory = os.path.join('acts',doc['status'].lower(), doc['title'][0].lower())
    filename = doc['title'].lower() + '.md'
    fullpath = os.path.join(directory, filename)
    fullpath = "".join(c for c in fullpath if c.isalnum() or c in keepcharacters).rstrip()
    converter.check_dir(directory)

    if os.path.exists(fullpath):
        print 'already converted {}'.format(filename)
        continue

    if doc['type'] not in ['iconDOC', 'iconDOCX', 'iconRTF']:
        message = 'Unable to convert {} of type {}'.format(doc['title'], doc['type'])
        with open(fullpath, 'wb') as out:
            out.write(message)
        print message
        continue

    result = converter.convert(input=os.path.join('comlaw',doc['uuid']), output=fullpath, type=doc['type'])
    if WRITE:
        try:
            with open(fullpath, 'wb') as out:
                out.write(result)
        except:
            os.remove(fullpath)
            raise
    else:
        print result

    print 'Converted {}'.format(fullpath)



