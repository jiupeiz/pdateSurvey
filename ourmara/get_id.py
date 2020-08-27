#! /usr/bin/python3
import urllib.request
import urllib.parse
import re
from tqdm import tqdm

browse_url = 'https://marathon.library.northeastern.edu/browse/'
ajax_url = 'https://marathon.library.northeastern.edu/wp-admin/admin-ajax.php'
browse_req = urllib.request.Request(browse_url, headers={"User-Agent": "Mozilla/5.0"})

browse_body = urllib.request.urlopen(browse_req).read()
nonce = re.search(r'"nonce":"(\w+)"', str(browse_body)).group(1)
idList = []
for page in tqdm(range(1,159)):
    data = urllib.parse.urlencode(
        {
            '_ajax_nonce': nonce,
            'action': 'get_browse',
            'params[per_page]': 50,
            'params[page]': page,
            'params[sort]': "system_modified_dtsi%20asc",
            'params[show_facets]': "false"
        }
    )

    data = data.encode('ascii')
    ajax_req = urllib.request.Request(ajax_url, headers={"User-Agent": "Mozilla/5.0"})
    ajax_response = urllib.request.urlopen(ajax_req, data).read()
    idListPage = re.findall(r'\"id\\\\":\\\\"(neu:\w+)\\\\', str(ajax_response))
    idList += idListPage

for id in idList:
    print(id)