#
# USAGE:
# 1. find some public company on macrotrends.net
# 2. run program with argument TICKER/company as seen in the url
#
from bs4 import BeautifulSoup
import sys
import requests

def main(company, metric):
    URL = 'https://www.macrotrends.net/stocks/charts/{company}/{metric}'.format(company=company, metric=metric)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    results = soup.find(id='style-1')
    job_elems = results.find_all('table', class_='historical_data_table table')

    table = job_elems[1].find('tbody')
    table_entries = table.find_all('td')

    dates = []
    metric  = []
    for i in range(len(table_entries)):
        if i%2 == 0:
            dates += [table_entries[i].text]
        else:
            metric += [table_entries[i].text]

    dates.reverse()
    metric.reverse()

    for r in metric: 
        print(r)

if __name__ == '__main__':
    print("REVENUE")
    main(sys.argv[1], 'revenue')
    print("GROSS PROFIT")
    main(sys.argv[1], 'gross-profit')

