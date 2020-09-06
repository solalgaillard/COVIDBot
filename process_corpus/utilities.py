import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
from nltk.tokenize.toktok import ToktokTokenizer
from process_corpus.contractions import CONTRACTION_MAP
import re
import spacy
import unicodedata
from urllib.parse import urlparse

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

'''
    Ici, nous regroupons toutes les fonctions utilitaires comme celles
    de normalisation du corpus, d'exportation, etc...
'''

'''
    Utilitaire nltk pour tokenisation et stopwords
'''
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')

'''
    Auto-descriptif
'''
def _remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

'''
    Transforme les contractions anglaises en formes longues
'''
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
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

'''
    Auto-descriptif
'''
def _remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

'''
    Auto-descriptif
'''
def _lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

'''
    Auto-descriptif
'''
def _remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

'''
    Fonction pilote avec valeurs par défaut. Prend le corpus entier
'''
def normalize_corpus(corpus_data, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=False):
    normalized_corpus = []
    # normalise chaque document
    for doc in corpus_data:
        # Enlève les accents
        if accented_char_removal:
            doc = _remove_accented_chars(doc)
        # Transforme les contractions en formes longues
        if contraction_expansion:
            doc = expand_contractions(doc)
        # Met le text en miniscule
        if text_lower_case:
            doc = doc.lower()
        # Enlève les retours à la ligne
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
        # lemmatise
        if text_lemmatization:
            doc = _lemmatize_text(doc)
        # Enlèvle les caractères spéciaux
        if special_char_removal:

            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = _remove_special_characters(doc, remove_digits=remove_digits)

        doc = re.sub(' +', ' ', doc)
        # Enlève les stopwords
        if stopword_removal:
            doc = _remove_stopwords(doc, is_lower_case=text_lower_case)
        normalized_corpus.append(doc)
    return normalized_corpus

'''
    Ici, on s'assure qu'une phrase ne peut pas être répétée dans plus
    de 40% des documents du même domaine. On évite ainsi les phrases
    institutionnelles qui peuvent s'être glissées dans le corpus.
'''
def remove_overused_sentences_from_corpus(corpus):
    sentences_to_occurences = {}
    filtered_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    # On itère sur toutes les entrées
    for idx, doc in enumerate(corpus["data"]):
        # On récupère le domaine du doc
        domain = urlparse(corpus['url'][idx]).netloc
        print(domain)
        # On initialise le nombre de doc par domaine
        if not domain in sentences_to_occurences:
            sentences_to_occurences[domain] = {"total_doc": 1}
        # Ou on incrémente
        else:
            sentences_to_occurences[domain]["total_doc"] += 1
        # On tokenise les phrases
        all_sentences = nltk.sent_tokenize(doc)

        # On incrémente ou initialise le compte par clé
        # dans dictionnaire.
        for sentence in all_sentences:
            if sentence in sentences_to_occurences[domain]:
                sentences_to_occurences[domain][sentence] += 1
            else:
                sentences_to_occurences[domain][sentence] = 1

    # On refait une passe pour vérifier le nombre de phrases apparaissant plusieurs
    # face au compte du nombre de document. Si dans le corpus, filtré par url, une
    # phrase est présente plus de 40% de fois, alors on ne le sauvegarde pas.
    for idx, doc in enumerate(corpus["data"]):
        tmp = ''
        domain = urlparse(corpus['url'][idx]).netloc
        all_sentences = nltk.sent_tokenize(doc)
        for sentence in all_sentences:
            if sentences_to_occurences[domain][sentence] / sentences_to_occurences[domain]["total_doc"] < 0.4:
                tmp = tmp + ' ' + sentence
        if (len(tmp) > 0):
            print(tmp)
            filtered_corpus['url'].append(corpus['url'][idx])
            filtered_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
            filtered_corpus['published_date'].append(corpus['published_date'][idx])
            filtered_corpus['data'].append(tmp.strip())
    print(filtered_corpus)
    return filtered_corpus


'''
    Retire les doubles entrées. Normalement le scrapper ne repasse jamais par la même
    url mais un même article peut être hébergé à differentes urls.
'''
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

'''
    Création d'un fichier xml en export pour labéliser le corpus
    d'entraînement
'''
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


'''
    Auto-descriptif
'''
def replace_xml_special_char(a_string):
    return a_string\
        .replace("&", "&amp;")\
        .replace("<", "&lt;")\
        .replace(">", "&gt;")\
        .replace('"', "&quot;")\
        .replace("'", "&apos;")


'''
    Après segmentation des documents, transformation de la
    structure de données pour s'assurer que les méta-données
    soient bien associées avec le nouveau segment.
'''
def each_segement_gets_description(corpus):
    filtered_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}

    # Chaque segment prend la description du parent.
    for idx, document in enumerate(corpus["data"]):
        for segment in document:
            filtered_corpus['url'].append(corpus['url'][idx])
            filtered_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
            filtered_corpus['published_date'].append(corpus['published_date'][idx])
            filtered_corpus['data'].append(segment)

    return filtered_corpus