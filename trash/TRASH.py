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

