import scrapy
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import w3lib.html
import pickle
from bs4 import BeautifulSoup
from scrapy.http import Request
import os.path
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from selenium.webdriver.common.by import By
import time

import os

#os.environ['WDM_LOCAL'] = '1'
home = str(Path.home())
os.environ["PATH"] += os.pathsep + f'{home}/.wdm/drivers/chromedriver/mac64/83.0.4103.39'
#print [name for name in os.listdir(".") if os.path.isdir(name)]

print(f'{home}/.wdm/drivers/chromedriver/mac64/83.0.4103.39')


class CovidSpider(CrawlSpider):
    name = "covidsources"
    allowed_domains = ["theguardian.com", "nytimes.com", "cdc.gov", "bbc.com"]
    start_urls = [
        "https://nytimes.com",
        #"https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2F",
        "https://theguardian.com",
        "https://www.cdc.gov/coronavirus/2019-ncov",
        "https://www.bbc.com/news/coronavirus",
    ]
    rules = ( #https://stackoverflow.com/questions/24890533/scray-crawlspider-doesnt-listen-deny-rules
        Rule(LinkExtractor(allow=('com/[\w_]+','gov/[\w_]+'), deny=('support','profile','job[s]?','about','comments','help','signout')),
             callback='parse_item'
             ),

    )

    count = { i : 0 for i in allowed_domains }
    max_entries_per_domain = 250
    todaysDate = datetime.datetime.now()
    base_path = Path(__file__).parent
    file_path = (base_path / "../../data/scrapped-data-binary.pickle").resolve()
    allFilesData = pickle.load(open(file_path, "rb+")) if os.path.isfile(file_path) else {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}



    def __init__(self, *a, **kw):
        super(CovidSpider, self).__init__(*a, **kw)
        #ATtention modify path and install in /user/.wmd
        webdriver.Chrome(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()

        #Prevent Download
        prefs = {
            "download.open_pdf_in_system_reader": False,
            "download.prompt_for_download": True,
            "plugins.always_open_pdf_externally": False
        }
        chrome_options.add_experimental_option(
            "prefs", prefs
        )



        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    '''
    def parse_start_url(self, args):
        print(args)
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=False)
    '''


    def cleanMe(self, html):
        soup = BeautifulSoup(html, "html.parser")  # create a new bs4 object from the html data loaded
        for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
            script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text


    def parse_item(self, response):
        self.driver.get(response.url)

        current_domain = next((x for x in self.allowed_domains if x in response.url), None)
        res = response.replace(body=self.driver.page_source)

        '''
            if response.url == 'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2F' :
            self.driver.find_element_by_id("username").send_keys("solalgaillard@yahoo.fr")
            self.driver.find_element_by_id("password").send_keys("Iw8nts0mejon0w!")
            self.driver.find_element_by_css_selector("button[data-testid='login-button'][type='submit']").click()
            time.sleep(10)# if flag by captcha
            yield Request(url='https://nytimes.com', callback=self.parse_item, dont_filter=False)
        
        '''



        if self.count[current_domain]<self.max_entries_per_domain:
            if response.url not in self.allFilesData['url']:
                tagsAllowedList = ["div", "article", "aside"]
                tags = []
                published_date = None

                if 'guardian' in response.url:
                    button = self.driver.find_elements_by_css_selector(".signin-gate__dismiss")
                    if len(button) > 0:
                        button[0].click()
                        time.sleep(10)  # if flag by captcha

                    published_date_search = re.search('theguardian\.com/\S*/(\d{4}/[A-z]{3}/\d{1,2})/\S+', response.url)
                    if published_date_search:
                        published_date = datetime.datetime.strptime(published_date_search.group(1), '%Y/%b/%d')
                    tags.extend(res.xpath(
                        "//*[contains(@class, 'content__article-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    tags.extend(res.xpath("//*[contains(@class, 'js-liveblog-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())


                elif 'bbc' in response.url:
                    tags.extend(res.xpath("//*[contains(@class, 'story-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    timestamp_elements = self.driver.find_elements_by_css_selector(".story-body .date")
                    if len(timestamp_elements) > 0:
                        published_date = datetime.datetime.fromtimestamp(int(timestamp_elements[0].get_attribute('data-seconds')))


                elif  'nytimes' in response.url:
                    tags.extend(res.xpath("//*[contains(@name, 'articleBody')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    published_date_search = re.search('nytimes\.com/(\d{4}/\d{2}/\d{1,2})/\S+', response.url)
                    if published_date_search:
                        published_date = datetime.datetime.strptime(published_date_search.group(1), '%Y/%m/%d')

                else:

                    for i in range(len(tagsAllowedList)):
                        tags.extend(res.xpath(
                            f"//{tagsAllowedList[i]}/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                        #tags.extend(res.css(f'{tagsAllowedList[i]} *::text').getall())


                    if 'cdc.gov' in response.url:
                        timestamp_elements = self.driver.find_elements_by_xpath("//meta[@property='cdc:last_updated']")
                        if len(timestamp_elements) > 0:
                             published_date = datetime.datetime.strptime(timestamp_elements[0].get_attribute('content'), '%B %d, %Y')


                if published_date and abs((self.todaysDate - published_date).days) < 90:
                    SENTENCE_PATTERN = re.compile(r'\S.+?[.!?]|[.!?][\'\"]\s+(?=\s+|$)+')  # make multiligne and comment https://stackoverflow.com/questions/5032210/php-sentence-boundaries-detection/5844564#5844564

                    FOUR_WORDS_TAG_MIN = re.compile(r'(\w+(?:\s+|[.!?]$)){4}')
#Change order of checks
                    document_sent_tok = re.findall(SENTENCE_PATTERN, ' '.join([self.cleanMe(tag) for tag in tags if re.search(FOUR_WORDS_TAG_MIN, tag)]).replace("\n"," "))

                    document = ' '.join([sent for sent in document_sent_tok ])

                                         #if re.search(THREE_WORDS_TAG_MIN, sent)]).replace("\s{2,}", " ")

                    #document= self.cleanMe(document) #Redondance mais important

                    if(len(document)>1000): #pas de micro documents
                        self.allFilesData['url'].append(response.url)
                        self.allFilesData['scrapped_date'].append(self.todaysDate)
                        self.allFilesData['published_date'].append(published_date)
                        self.allFilesData['data'].append(document)
                        with open(self.file_path, 'wb') as f: #NOT GOOD, NEEDS TO BE INVOKED ONLY ONCE AT THE END NEED A PANDAFRAME
                            pickle.dump(self.allFilesData, f)
                        self.count[current_domain] += 1

            #yield from res.follow_all(css='a', callback=self.parse)