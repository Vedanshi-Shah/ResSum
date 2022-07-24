# Parse the text from json file
# Look for Text attribute in elements object
import json
import re

# TODO: Make hyperlinks regex

# Define regexes
# remove information about figures and tables from text
fig = re.compile(r"Figure [0-9]+:")
table = re.compile(r"Table [0-9]+:")
# empty links
links = re.compile(r"\(<>\)")
# (...)
ellipsis = re.compile("\([.]+\)")
# references and numbers in ()
references_rounds = re.compile(r"\([a-zA-Z,.;\- ]*[0-9]+[^\)]*\)")
# references and numbers in []
references_square = re.compile(r"\[[a-zA-Z,.;\- ]*[0-9]+[^\]]*\]")
# references and numbers in {}
references_curly = re.compile(r"{[a-zA-Z,.;\- ]*[0-9]+[^}]*}")
# sentences with greek letters
greek = re.compile(r"[^.]*[α-ωΑ-Ω][^.]*.")
# hyperlinks
hyperlinks = re.compile(r"(https:)[^ ]+")
# Alphabets
alpha = re.compile(r"[A-Z a-z]+")

def read_file(NAME, encoding="utf-8"):
    with open(f"{NAME}.json", "r", encoding=encoding) as f:
        data = json.loads(f.read())
    f.close()
    return data['elements']

def parse_txt(NAME):
    with open(f"{NAME}.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    f.close()
    out_data = ""
    sections = {}
    prevHeader = ""
    for element in data['elements']:
        if '/Document/H1' in element['Path']:
            heading = element.get("Text", "")
            if (heading!=""):
                heading = re.findall(alpha, heading)[0].strip().title()
                print(heading)
                sections[heading] = ""
                prevHeader = heading
        if 'Document/H2' in element['Path']:
            if (prevHeader!=""):
                heading  = element.get('Text', "").strip().title()
                text = f"\n ### {heading}  "
                sections[prevHeader] += text
        if 'Document/H3' in element['Path']:
            if prevHeader!="":
                heading  = element.get('Text', "").strip().title()
                text = f"\n #### {heading}  "
                sections[prevHeader] += text
        if '/Document/P' in element['Path']:
            if prevHeader!="":
                text = element.get('Text', "")
                sections[prevHeader] += f"{text}  "
    tmp_sections = {}
    for section, section_txt in sections.items():
        tmp_sections[section] = parser(section_txt)
    with open("sections.json", "w") as f:
        json.dump(tmp_sections, f, indent=4)
    f.close()
    
def parser(txt):
    txt = re.sub(links, "", txt)
    txt = re.sub("\n", "", txt)
    # Comment if does not work
    # txt = txt[txt.lower().find('abstract'):]
    txt = re.sub("-", " ", txt)
    txt = re.sub(references_rounds, "", txt)
    txt = re.sub(references_square, "", txt)
    txt = re.sub(references_curly, "", txt)
    txt = re.sub(ellipsis, "", txt)
    txt = re.sub(greek, "", txt)
    return txt

def write_file(txt, NAME, encoding="utf-8"):
    with open(f'{NAME}.txt', "w", encoding=encoding) as f:
        f.write(txt)
    f.close()

def sectionify(NAME):
    with open(f"{NAME}.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    f.close()
    sections = {}
    prevHeader = ""
    for element in data['elements']:
        if '/Document/H1' in element['Path']:
            sections[element.get('Text', "")] = ""
            prevHeader = element.get('Text', "")
        if 'Document/H2' in element['Path']:
            if (prevHeader!=""):
                # print(element.get('Text', "None"))
                head = element.get('Text', "")
                text = f"\n ### {head}\n"
                sections[prevHeader] += text
        if '/Document/P' in element['Path']:
            if (prevHeader!=""):
                sections[prevHeader] += element.get('Text', "")
    with open("sections.json", "w") as f:
        json.dump(sections, f, indent=4)
    f.close()

def parse(NAME):
    print("Parsing")
    # data = read_file(NAME)
    parse_txt(NAME)
    # write_file(txt, NAME)



# ------------------------------- DON'T CONDEMN THE PAST -------------------------------=
# parser:
# for element in elements:
        # # Check for Text attribute. Don't take anything after encountering references as a heading
        # if 'Text' in element and element['Text'].lower().strip()=="references":
        #     #print("Here")
        #     break
        # if 'Text' in element and ('/Document' in element['Path'] or element['Text'].lower().strip()=="abstract"):
        #     figu = re.search(fig, element['Text'])
        #     tablu = re.search(table, element['Text'])
        #     if (figu or tablu):
        #         continue
        #     out_data += "\n" + element['Text']
