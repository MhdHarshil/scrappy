import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from collections import deque



class Crawl():
    def __init__(self, url, key_word) -> None:
        self.new_url = deque([(url, 0)])
        self.all_url_log = open("all_url_log.txt", "w+")
        self.processed_url = set()
        self.key_word = key_word
        pass

    def bfs_url_crawler(self):
        url_count = 0
        stop_flag = 0
        local_urls = set()


        while len(self.new_url) and not stop_flag:
            if len(self.new_url) > 1000:
                stop_flag = 1
            
            # pop the url and put all the nei in the q
            pop_val = self.new_url.popleft()
            url, cur_level = pop_val
            info = f"url: {url} - depth level: {cur_level}\n"
            
            # write in txt file
            self.all_url_log.write(info)

            # Adding Processed URL's and Updating the list classes
            # Processes the entering values and Get the result by the way
            self.processed_url.add(url)
            
            url_count += 1

            # Log writter for cli

            if cur_level > 2:
                print("Url Out of Scope")
                continue


            try:
                response = requests.get(url)
            except:
                print("Broken URL, Error 404")
                continue
            
            url_parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(url_parts)
            soup = BeautifulSoup(response.text, 'lxml')

            for link in soup.find_all('a'):
                anchor_link = link.get('href')
                if anchor_link.startswith('/'):
                    local_link = f"{base_url}{anchor_link}"
                else:
                    local_link = anchor_link

                print(local_link)

                if local_link not in self.processed_url:
                    self.new_url.append((local_link, cur_level+1))






if __name__ == "__main__":

    url = "https://www.mayoclinic.org/diseases-conditions"

    path_level = ["index"]

    key_word = ["disease-conditions"]

    crawler = Crawl(url, key_word)
    crawler.bfs_url_crawler()
