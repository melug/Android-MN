import sys
import os.path

from lxml import etree

manifest_file = 'AndroidManifest.xml'

def find_projects(dr):
    files = os.listdir(dr)
    if manifest_file in files:
        yield dr
    else:
        for f in files:
            sub_dr = os.path.join(dr, f)
            if os.path.isdir(sub_dr):
                for project in find_projects(sub_dr):
                    yield project

def extract_string_resource(project_dir):
    strings_filepath = os.path.join(project_dir, 'res/values/strings.xml')
    with open(strings_filepath, 'r') as f:
        text = f.read()
    tree = etree.fromstring(text)
    for string_tag in tree.xpath('/resources/string'):
        print '+-', string_tag.attrib['name'], string_tag.text

if __name__ == '__main__':
    if len(sys.argv) == 2:
        for project_path in find_projects(sys.argv[1]):
            print 'Found project at:', project_path
            print '|'
            try:
                extract_string_resource(project_path)
            except:
                pass
            print '+' + '-'*140
    
