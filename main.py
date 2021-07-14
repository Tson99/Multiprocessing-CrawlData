from multiprocessing import Pool
import bs4 as bs
import random
import requests
import string
import yaml


class CrawlData(object):
    def __init__(self):
        super(CrawlData, self).__init__()
        with open('configs.yaml') as file:
            self._config = yaml.full_load(file)

    @staticmethod
    def handle_local_links(url, link):
        if link.startswith('/'):
            return ''.join([url, link])
        else:
            return link

    def _get_links(self, url):
        try:
            resp = requests.get(url)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            body = soup.body
            links = [link.get('src') for link in body.find_all('img')]
            links = [self.handle_local_links(url, link) for link in links]
            links = [str(link.encode("ascii")) for link in links]
            print(links)
            return links
        except TypeError as e:
            print(e)
            print('Got a TypeError, probably got a None that we tried to iterate over')
            return []
        except IndexError as e:
            print(e)
            print('We probably did not find any useful links, returning empty list')
            return []
        except AttributeError as e:
            print(e)
            print('Likely got None for links, so we are throwing this')
            return []
        except Exception as e:
            print(str(e))
            return []

    def start(self):
        p = Pool(processes=self._config['process'])
        data = p.map(self._get_links, (url for url in self._config['urls']))
        data = [url for url_list in data for url in url_list]
        p.close()

        with open('urls.txt', 'w') as f:
            f.write(str(data))


if __name__ == '__main__':
    crawler = CrawlData()
    crawler.start()
