import os
import psycopg2
import requests
import re

#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#cursor=conn.cursor()

categoryFile = requests.get('https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/README.md')
categoryFile = categoryFile.text
categoryFile = categoryFile.replace("####", "###")
categoryFile = categoryFile.splitlines()
check = False
text = ""
for line in categoryFile:
    if line == "### Books":
        check = True
    elif line == "## License":
        check = False
        break
    if check and line[:1] == "#":
        line = line.replace("### ", "")
        text += "\n*" + line + "*\n"
    
    if check and re.findall(r'[^\(]+\.md(?=\))', line):
        tmp = re.findall(r'[^\(]+\.md(?=\))', line)
        text += "`" + tmp[0] + "`\n"

print(text)