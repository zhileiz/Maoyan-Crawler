import requests
import re
import io
import json
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
           return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'rank': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }
def write_to_file(content):
    with io.open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()

def main(int):
    if int == 0:
        url = "http://maoyan.com/board/4"
    else:
        url = "http://maoyan.com/board/4?offset=" + str(int)
    html = get_one_page(url)
    parse_page(html)
    for item in parse_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(10*i)