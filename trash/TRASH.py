'''
        cleanedUpTags = []
        NEW_LINES_PATTERN = re.compile(r'\n+')
        WHITE_SPACE_PATTERN = re.compile(r'\s+')
        SENTENCE_PATTERN = re.compile(
            r'\S.+?[.!?]|[.!?][\'\"]\s+(?=\s+|$)+')  # make multiligne and comment https://stackoverflow.com/questions/5032210/php-sentence-boundaries-detection/5844564#5844564

        for x in tags:
            tmpValue = re.sub(NEW_LINES_PATTERN, ' ', w3lib.html.remove_tags(x).strip())
            tmpValue = re.sub(WHITE_SPACE_PATTERN, ' ', tmpValue.strip())
            cleanedUpTags.append(tmpValue)

        THREE_WORDS_SENTENCE_MIN = re.compile(r'(\w+(?:\s+|[.!?]$)){3}')
        tmp = ''
        for textBetweenTags in tags:
            if len(textBetweenTags) > 500:
                newsentence = re.findall(SENTENCE_PATTERN, textBetweenTags)
                if len(newsentence) > 0:
                    tmp = tmp + ' ' + (' '.join([x for x in newsentence if (re.search(THREE_WORDS_SENTENCE_MIN, x))]))

        soup = BeautifulSoup(tmp)
        [s.extract() for s in soup(["html", "script", "style"])]
        tmp = w3lib.html.remove_tags(str(soup))


        output = re.sub(r"/|:", "-", response.url)
        with open(f'{output}.txt', 'w') as filehandle:
            for sentence in tags:
                newsentence = re.findall(SENTENCE_PATTERN, sentence)
                if len(newsentence) > 0:
                    print(newsentence, re.search(THREE_WORDS_SENTENCE_MIN, newsentence[0]))
                filehandle.writelines("%s " %x for x in newsentence if(re.search(THREE_WORDS_SENTENCE_MIN, x)) )

'''

# chrome_options.add_argument("--incognito")
# webdriver.Chrome(executable_path=f'{home}/.wdm/drivers/chromedriver/mac64/83.0.4103.39/chromedriver')


for idx, value in enumerate(lookForSentences):
    if (re.search(THREE_WORDS_SENTENCE_MIN, value)):
        document = document + (" " if idx == 0 else "") + value

        # tags.extend(res.css('.story-body *::text').getall())
    # SENTENCE_PATTERN = re.compile(
    # r'\S.+?[.!?]|[.!?][\'\"]\s+(?=\s+|$)+')  # make multiligne and comment https://stackoverflow.com/questions/5032210/php-sentence-boundaries-detection/5844564#5844564

    THREE_WORDS_SENTENCE_MIN = re.compile(r'(\w+(?:\s+|[.!?]$)){3}')

    document = ''
    for tag in tags:
        # if len(tag) > 20: #pas de micro tags
        # lookForSentences = re.findall(SENTENCE_PATTERN, tag)
        # print(lookForSentences)
        # if len(lookForSentences) > 0:
        document = document + ' ' + ' '.join(
            [value for value in lookForSentences if re.search(THREE_WORDS_SENTENCE_MIN, value)])


'''
To measure similarity, create matrix between sentences and compare them all, rank rows per
published_date, then per source. Need dataframeAccrossBoard

'''


'''
def cluster_sentences(sentences, nb_of_clusters=5):
    tfidf_vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize,
                                       max_df=0.9,
                                       min_df=0.1)
    # builds a tf-idf matrix for the sentences
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpusManipulation.normalize_corpus(sentences))
    kmeans = KMeans(n_clusters=nb_of_clusters)
    kmeans.fit(tfidf_matrix)
    clusters = collections.defaultdict(list)
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(i)
    return dict(clusters)


def truc():
    sentences = ["Nature is beautiful", "I like green apples",
                 "We should protect the trees", "Fruit trees provide fruits",
                 "Green apples are tasty"]
    nclusters = 3
    clusters = cluster_sentences(sentences, nclusters)
    print(clusters)
    print("test2")
    for cluster in range(nclusters):
        print("cluster ", cluster, ":")
        for i, sentence in enumerate(clusters[cluster]):
            print("\tsentence ", i, ": ", sentences[sentence])


'''

'''
for noun in list(dict.fromkeys(nounIndices)):
    print(noun)
    for verb in list(dict.fromkeys(verbIndices)):
        print(verb)
        statements = textacy.extract.semistructured_statements(segment, noun, cue=verb)
        for statement in statements:
            allStatements.add(statement)

for statement in allStatements:
    entity, cue, fact = statement
    print("* entity:", entity, ", cue:", cue, ", fact:", fact)
'''