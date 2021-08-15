from requests_html import HTMLSession
import os
import pandas as pd

s = HTMLSession()

data = []

def page(x):
    url = f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={keyword}&refinements=ContentType:Journals&pageNumber={x}'
    response = s.get(url)
    response.html.render(sleep=8, timeout=300, keep_page=True)
    contents = response.html.find('div.List-results-items')
    for item in contents:
        Title = item.find('h2', first=True).text
        Author = item.find('p', first=True).text
        Year = item.find('div.publisher-info-container span', first=True).text.split(':')[-1]
        Journal = item.find('div.description a', first=True).text
        Abstract = item.find('div.js-displayer-content span', first=True).text
        dict = {
            'Title':Title,
            'Author':Author,
            'Year':Year,
            'Journal':Journal,
            'Abstract':Abstract
        }
        data.append(dict)
    return data

keyword = input('Enter keyword: ')   
for x in range(1, 4):
    page(x)
    
df = pd.DataFrame(data)
df.to_csv(f'{keyword}.csv', index=False)
print('fin')