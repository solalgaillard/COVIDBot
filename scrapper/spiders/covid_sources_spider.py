from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import pickle
from bs4 import BeautifulSoup
import os.path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import time
import os
import datetime


'''
    Définition du scrapper.
    4 urls de références, le nytimes, le guardian, le site du cdc et le site de la bbc.
    On charge les données existantes dans all_files_data et on scrappe à nouveau avec
    un maximum de 250 valeurs par domaine. On installe le driver pour Chrome s'il n'existe pas
    et on ajoute l'executable à la variable PATH à l'instanciation, on passe aussi les options au driver.
'''
class CovidSpider(CrawlSpider):
    '''
       Propriétés de la classe, certaines parsées par l'objeet parent de Scrapy.
    '''
    name = "covidsources"
    allowed_domains = ["theguardian.com", "nytimes.com", "cdc.gov", "bbc.com"]

    # Bizarrement, j'avais toute une stratégie pour contourner le paywall du NYTimes mais cela ne semble pas
    # nécessaire, il doit y avoir un script JavaScript qui obfusque le contenu après.
    start_urls = [
        "https://nytimes.com",
        #"https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2F",
        "https://theguardian.com",
        "https://www.cdc.gov/coronavirus/2019-ncov",
        "https://www.bbc.com/news/coronavirus",
    ]
    # Filtre les url contenant les mots clés suivant.
    rules = ( #https://stackoverflow.com/questions/24890533/scray-crawlspider-doesnt-listen-deny-rules
        Rule(LinkExtractor(allow=('com/[\w_]+','gov/[\w_]+'), deny=('support','profile','job[s]?','about','comments','help','signout')),
             callback='parse_item'
             ),

    )

    count = { i : 0 for i in allowed_domains }
    max_entries_per_domain = 250
    todays_date = datetime.datetime.now()
    file_path = (Path(__file__).parent / "../../data_saved/scrap.pickle").resolve()
    all_files_data = pickle.load(open(file_path, "rb+")) if os.path.isfile(file_path) else {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}


    '''
        Propriétés de l'objet, notamment instanciation du driver et des options de celui-ci
    '''
    def __init__(self, *a, **kw):
        super(CovidSpider, self).__init__(*a, **kw)
        # Installe in ./.wmd
        os.environ['WDM_LOCAL'] = '1'
        # Récupère l'URL
        driver_path = ChromeDriverManager().install()
        # Et ajoute le dans le PATH
        os.environ["PATH"] += os.pathsep + driver_path[:driver_path.rfind('/')]
        #self.driver = webdriver.Chrome(driver_path)
        # Ajoute les options pour Chrome pour empêcher les téléchargements automatiques ou l'ouverture
        # d'autres processus.
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


        # Instancie le driver
        self.driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)


    '''
        Nettoie les balises html restés dans les chaînes après sc
    '''
    def _clean_me(self, html):
        # crée un nouvel objet bs avec l'html passé
        soup = BeautifulSoup(html, "html.parser")
        # Enlève les balises script et style
        for script in soup(["script", "style"]):
            script.extract()
        # Prend le texte
        text = soup.get_text()
        # Fait une liste avec une entrée pour chaque retour à la ligne
        # Enlève les espaces en début et fin de ligne.
        lines = (line.strip() for line in text.splitlines())
        # Ségmente les multiespaces en lignes séparées
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Enlève les lignes vides.
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    '''
        Fonction appelé à chaque nouvelle URL parsée. Dépendent du domaine, ce ne sont pas les même règles
        pour extraire le contenu. On récupère aussi les dates de publications. Il a fallu réaliser une analyse
        pour chaque domaine.
    '''
    def parse_item(self, response):

        # Fais passer l'url au driver
        self.driver.get(response.url)

        # Prend le domaine
        current_domain = next((x for x in self.allowed_domains if x in response.url), None)

        #Override la réponse par le driver de selenium
        res = response.replace(body=self.driver.page_source)

        # Tant qu'on a pas dépassé le nombre d'entrées max par domaine
        if self.count[current_domain]<self.max_entries_per_domain:
            if response.url not in self.all_files_data['url']:
                tags_allowed_list = ["div", "article", "aside"]
                tags = []
                published_date = None

                # Pour le guardian
                if 'guardian' in response.url:
                    # Se débarasse de la bannière qui bloque le contenu
                    button = self.driver.find_elements_by_css_selector(".signin-gate__dismiss")
                    if len(button) > 0:
                        button[0].click()
                        time.sleep(10)  # laisse le temps de se débarasser de la bannière

                    # Extrait la date de l'article et la parse
                    published_date_search = re.search('theguardian\.com/\S*/(\d{4}/[A-z]{3}/\d{1,2})/\S+', response.url)
                    if published_date_search:
                        published_date = datetime.datetime.strptime(published_date_search.group(1), '%Y/%b/%d')
                    # Récupère le contenu
                    tags.extend(res.xpath(
                        "//*[contains(@class, 'content__article-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    tags.extend(res.xpath("//*[contains(@class, 'js-liveblog-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())

                # Pour la BBC
                elif 'bbc' in response.url:
                    # Récupère le contenu
                    tags.extend(res.xpath("//*[contains(@class, 'story-body')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    # Récupère la date de publication
                    timestamp_elements = self.driver.find_elements_by_css_selector(".story-body .date")
                    if len(timestamp_elements) > 0:
                        published_date = datetime.datetime.fromtimestamp(int(timestamp_elements[0].get_attribute('data-seconds')))

                # Pour le NYTimes
                elif 'nytimes' in response.url:
                    # Récupère le contenu
                    tags.extend(res.xpath("//*[contains(@name, 'articleBody')]/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                    # Récupère la date de publication
                    published_date_search = re.search('nytimes\.com/(\d{4}/\d{2}/\d{1,2})/\S+', response.url)
                    if published_date_search:
                        published_date = datetime.datetime.strptime(published_date_search.group(1), '%Y/%m/%d')

                # Pour le reste
                else:
                    # Parse les balises acceptées
                    for i in range(len(tags_allowed_list)):
                        #Exclue les scripts
                        tags.extend(res.xpath(
                            f"//{tags_allowed_list[i]}/descendant-or-self::*[not(self::script or self::style)]/text()").getall())
                        #tags.extend(res.css(f'{tags_allowed_list[i]} *::text').getall())

                    # Récupère la date de publication pour le CDC
                    if 'cdc.gov' in response.url:
                        timestamp_elements = self.driver.find_elements_by_xpath("//meta[@property='cdc:last_updated']")
                        if len(timestamp_elements) > 0:
                             published_date = datetime.datetime.strptime(timestamp_elements[0].get_attribute('content'), '%B %d, %Y')

                # Sélectionne que les entrées qui ont été publiées dans les trois derniers mois.
                # Utilise regex pour isoler les phrases, pas Spacy ou nltk.
                if published_date and abs((self.todays_date - published_date).days) < 90:
                    # Les phrases devaient pouvoir contenir multiligne et commentaire. Custom Tokenization!
                    # https://stackoverflow.com/questions/5032210/php-sentence-boundaries-detection/5844564#5844564
                    SENTENCE_PATTERN = re.compile(r'\S.+?[.!?]|[.!?][\'\"]\s+(?=\s+|$)+')

                    # Vérifie qu'il y a au moins 4 mots.
                    FOUR_WORDS_TAG_MIN = re.compile(r'(\w+(?:\s+|[.!?]$)){4}')

                    # Pour chaque tag, remets les retours à la ligne sur la même ligne, vérifie qu'il y a 4 mots,
                    # Nettoie les tags, puis extrait tous les tags en un document puis
                    # extrait tout les segments du texte qui pésentent la forme d'une phrase.
                    document_sent_tok = re.findall(SENTENCE_PATTERN, ' '.join([self._clean_me(tag) for tag in tags if re.search(FOUR_WORDS_TAG_MIN, tag)]).replace("\n"," "))

                    # Puis reconstruit un document.
                    document = ' '.join([sent for sent in document_sent_tok ])

                    # Aucun micro document ne peut être sélectionné.
                    if(len(document)>1000):
                        self.all_files_data['url'].append(response.url)
                        self.all_files_data['scrapped_date'].append(self.todays_date)
                        self.all_files_data['published_date'].append(published_date)
                        self.all_files_data['data'].append(document)
                        self.count[current_domain] += 1