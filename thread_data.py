import httpx as r
import pandas as pd

from selectolax.parser import HTMLParser

url = 'https://www.cassandramdias.com/dmc-colors-to-rgb-conversion-chart'

response = r.get(url)

rows = HTMLParser(response.text).css('tr')

dmc_data = {
    'code': [],
    'name': [],
    'r': [],
    'g': [],
    'b': [],
    'hex': [],
}

for row in rows[2:]:
    row_content = [cell.text() for cell in row.css('td')]
    try:
        dmc_data['code'].append(row_content[0])
        dmc_data['name'].append(row_content[1])
        dmc_data['r'].append(row_content[2])
        dmc_data['g'].append(row_content[3])
        dmc_data['b'].append(row_content[4])
        dmc_data['hex'].append(row_content[5])
    except IndexError:
        print(row_content)

df = pd.DataFrame(dmc_data)
df.to_parquet('data/data.parquet', index=False)
