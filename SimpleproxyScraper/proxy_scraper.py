'''
Proxy Scraper

@Andrea-Tomatis
'''


import requests
from bs4 import BeautifulSoup



class Scraper():

    @staticmethod
    def getSite(url):
        response = requests.get(url)
        Scraper.check_response(response)
        refBody = BeautifulSoup(response.content, 'html.parser')
        proxy_list = refBody.find_all('table')
        return proxy_list[0].find_all('tbody')[0].find_all('tr')
    
    @staticmethod
    def find_list(rows):
        print('proxies reading...')
        proxy_lst = []

        for row in rows:
            try:
                valid_proxy = (
                    row.findAll('td')[0].find_all('script')[0].text[16:-3],
                    row.findAll('td')[1].text.replace(' ','').replace('\n',''),
                    row.findAll('td')[3].find_all('small')[0].text.replace(' ',''),
                    row.findAll('td')[4].find_all('span')[0].text.replace(' ',''),
                    row.findAll('td')[5].find_all('a')[0].text.replace(' ','').replace('\n',''),
                    row.findAll('td')[6].find_all('span')[0].text.replace(' ','')
                )
                proxy_lst.append(valid_proxy)
            except:
                print('invalid proxy')
        
        return proxy_lst
    

    @staticmethod
    def check_response(response):
        if response.status_code != 200:
            print('error: page not found')
            exit(-1)

    
    @staticmethod
    def proxy_test(proxy):
        #test each proxy on whether it access api of hh.ru
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        try:
            params = {
                'text': f'NAME:C++',
                'area': 113,
                'page': 0,
                'per_page': 100
            }
            requests.get('https://api.hh.ru/vacancies', headers=headers, proxies={'http' : proxy}, timeout=1, params=params)
            final.append(proxy)
        except:
            pass
        return proxy
    


def main():
    el = Scraper.find_list(Scraper.getSite('https://www.proxynova.com/proxy-server-list/'))
    print(Scraper.proxy_test(el[0]))#test every proxy

if __name__ == '__main__':
    main()
