#
# USAGE:
# 1. find some public company on macrotrends.net
# 2. run program with argument TICKER/company as seen in the url
#
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests

internet_services = 'https://www.macrotrends.net/stocks/industry/213/internet-services'
internet_commerce = 'https://www.macrotrends.net/stocks/industry/211/internet-commerce'
# computer software: https://www.macrotrends.net/stocks/industry/44/computer-software

def isTableEntry(tag):
    return tag.has_attr('role') and tag.has_attr('id')

def main():
    links = pd.read_csv('urls.csv', '\n')
    data = pd.DataFrame()
    for link in links['links']:
        company = link[42:-20]
        company_data = getCompanyMetrics(company)
        
        data = pd.concat([data, company_data])

    data.to_csv('out.csv')

def getCompanyMetrics(company):
    revenueURL = 'https://www.macrotrends.net/stocks/charts/{company}/revenue'.format(company=company)
    grossprofitURL = 'https://www.macrotrends.net/stocks/charts/{company}/gross-profit'.format(company=company)

    df = pd.DataFrame()

    for url in [('quarterly_revenue_mil', revenueURL), ('gross_profit_mil', grossprofitURL)]:
        page = requests.get(url[1])

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
                metric += [table_entries[i].text[1:].replace(',', '')]

        dates.reverse()
        metric.reverse()

        df['date'] = dates
        df['company'] = company[company.find('/')+1:]
        df[url[0]] = metric
    
    # remove rows w/ empty string values
    df = df[df['quarterly_revenue_mil'] != '']
    
    # convert numerical types to int
    df = df.astype({'quarterly_revenue_mil': 'int32', 'gross_profit_mil': 'int32'})

    # add gross margin % col
    df['gross_margin'] = df['gross_profit_mil'] / df['quarterly_revenue_mil']
    return df

if __name__ == '__main__':
    main()
