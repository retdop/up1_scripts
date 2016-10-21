import sys
import requests
from lxml import html

def download_file(download_url):
    r = requests.get(download_url, stream=True)
    with open( './' + download_url.split('/')[-1] + '.pdf', 'wb') as f:
        f.write(r.content)
    print("Completed")

extension = 'pdf'
if len(sys.argv) > 2:
    extension = sys.argv[1]
    html_page = sys.argv[2]

page = requests.get(html_page).text
doc = html.fromstring(page)

bad_links = 0
for link in doc.cssselect("a"):
    try :
        # print(link.text_content())
        # print(link.attrib['href'][(-1 * len(extension)):])
        if link.attrib['href'][-1 * len(extension):] == extension:
            # print(link.attrib['href'])
            download_file(link.attrib['href'])
    except:
        bad_links += 1

print('bad_links', bad_links)
