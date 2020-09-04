import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
from nltk.tokenize.toktok import ToktokTokenizer
from process_corpus.contractions import CONTRACTION_MAP
import re
import spacy
import unicodedata

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')


def _remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def _expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def _remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def _lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

def _remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def normalize_corpus(corpus_data, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=False):
    normalized_corpus = []
    # normalize each document in the corpus
    for doc in corpus_data:
        # remove accented characters
        if accented_char_removal:
            doc = _remove_accented_chars(doc)
        # expand contractions
        if contraction_expansion:
            doc = _expand_contractions(doc)
        # lowercase the text
        if text_lower_case:
            doc = doc.lower()
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
        # lemmatize text
        if text_lemmatization:
            doc = _lemmatize_text(doc)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = _remove_special_characters(doc, remove_digits=remove_digits)
            # remove extra whitespace
        doc = re.sub(' +', ' ', doc)
        # remove stopwords
        if stopword_removal:
            doc = _remove_stopwords(doc, is_lower_case=text_lower_case)
        normalized_corpus.append(doc)
    return normalized_corpus


def remove_overused_sentences_from_corpus(corpus_data):
    sentences_to_occurences = {}
    for doc in corpus_data:
        all_sentences = nltk.sent_tokenize(doc)
        for sentence in all_sentences:
            if sentence in sentences_to_occurences:
                sentences_to_occurences[sentence] += 1
            else:
                sentences_to_occurences[sentence] = 1

    filtered_corpus = []
    for doc in corpus_data:
        tmp = ''
        all_sentences = nltk.sent_tokenize(doc)
        for sentence in all_sentences:
            if sentences_to_occurences[sentence] / len(corpus_data) < 1:
                tmp = tmp + ' ' + sentence
        if (len(tmp) > 0):
            filtered_corpus.append(tmp)

    return filtered_corpus

def remove_duplicates_in_corpus(corpus):
    docs_to_occurences = {}
    filtered_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    for idx, doc in enumerate(corpus['data']):
        if doc not in docs_to_occurences:
            filtered_corpus['url'].append(corpus['url'][idx])
            filtered_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
            filtered_corpus['published_date'].append(corpus['published_date'][idx])
            filtered_corpus['data'].append(doc)
            docs_to_occurences[doc] = True
    return filtered_corpus

# Base pour isoler données et créer un premier corpus d'entraînement
def export_scrapped_data_to_file_for_labeling(corpus, file_path, iteration):
    with open(file_path, 'w') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n\t<documents>\n")
        i = 0 ; k = 0
        while(k<iteration and i<len(corpus['data'])):
            f.write("\t\t<doc>\n\t\t\t<url>%s</url>" % (
                corpus['url'][i]))
            j = 0
            while (k < iteration and j<len(corpus['data'][i])):
                f.write(
                    "\n\t\t\t<data>\n\t\t\t\t<segment>%s</segment>"
                    "\n\t\t\t\t<label></label>\n\t\t\t</data>" % replace_xml_special_char(
                        corpus['data'][i][j]
                    )
                )
                j += 1 ; k += 1
            f.write("\n\t\t</doc>\n")
            i += i
        f.write("\t</documents>")

def replace_xml_special_char(a_string):
    return a_string\
        .replace("&", "&amp;")\
        .replace("<", "&lt;")\
        .replace(">", "&gt;")\
        .replace('"', "&quot;")\
        .replace("'", "&apos;")


def each_segement_gets_description(corpus):
    filtered_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}

    # Each segment gets their own description based on parent
    for idx, document in enumerate(corpus["data"]):
        for segment in document:
            filtered_corpus['url'].append(corpus['url'][idx])
            filtered_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
            filtered_corpus['published_date'].append(corpus['published_date'][idx])
            filtered_corpus['data'].append(segment)

    return filtered_corpus