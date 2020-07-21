import spacy
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pickle
nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
from process_corpus.utilities import ManipulateCorpus
from process_corpus.segment_documents import SegmentDocuments
from process_corpus.solve_coreferences import solveCoreference
from process_corpus.extract_features import featureExtractions
from process_corpus.extract_facts import ExtractFacts
from pathlib import Path
base_path = Path(__file__).parent
corpusManipulation = ManipulateCorpus()
solve_coreference = solveCoreference()
segment_documents = SegmentDocuments()


'''
file_path = (base_path / "../data/scrapped-data-binary.pickle").resolve()
corpus = pickle.load(open(file_path, "rb" ))
corpus = corpusManipulation.removeDuplicatesInCorpus(corpus)
print(len(corpus["data"]))
#corpus['data'] = corpusManipulation.removeOverUsedSentencesFromCorpus(corpus['data'])
corpus['data'] = [segment_documents.segmentDocs(solve_coreference.replaceOnlySentencesApart(document)) for document in corpus['data']]



corpusManipulation.exportScrappedDataToFile2(corpus)


feature_extractions = featureExtractions()


#feature_extractions.trainModelLogRegr()

feature_extractions.trainModelSVC()



filteredCorpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}


for idx, document in enumerate(corpus["data"]):
    for segment in document:
        filteredCorpus['url'].append(corpus['url'][idx])
        filteredCorpus['scrapped_date'].append(corpus['scrapped_date'][idx])
        filteredCorpus['published_date'].append(corpus['published_date'][idx])
        filteredCorpus['data'].append(segment)




filteredCorpus = feature_extractions.useModel(filteredCorpus)
print(filteredCorpus)


print(len(filteredCorpus["data"]), len(corpus["data"]))

file_path = (base_path / "../data/cleaned-up-corpus.pickle").resolve()
with open(file_path, 'wb+') as f:
    pickle.dump(filteredCorpus, f)
'''

'''
file_path = (base_path / "../data/cleaned-up-corpus.pickle").resolve()
filteredCorpus = pickle.load(open(file_path, "rb" ))

corpusManipulation.exportScrappedDataToFile(filteredCorpus)

#flatten = lambda l: [item for sublist in l for item in sublist]


#TODO - Opearation ici, c'est df avec chaque segment



feature_extractions = featureExtractions()
resultTopics = feature_extractions.featureExtraction(filteredCorpus["data"])
'''

file_path = (base_path / "../data/cleaned-up-corpus.pickle").resolve()
filteredCorpus = pickle.load(open(file_path, "rb" ))

file_path = (base_path / "../data/result-topic.pickle").resolve()
resultTopics = pickle.load(open(file_path, "rb" ))

extractFacts = ExtractFacts()

for topic_idx, topic in enumerate(resultTopics["topic_mapping"]):
    if topic:
        corpus_per_topic = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for cluster_idx, cluster in enumerate(resultTopics["clusters"]):
            if cluster == topic_idx:
                corpus_per_topic['url'].append(filteredCorpus['url'][cluster_idx])
                corpus_per_topic['scrapped_date'].append(filteredCorpus['scrapped_date'][cluster_idx])
                corpus_per_topic['published_date'].append(filteredCorpus['published_date'][cluster_idx])
                corpus_per_topic['data'].append(filteredCorpus["data"][cluster_idx])
        #create a file
        #process
        extractFacts.extract(corpus_per_topic)



#pd.DataFrame(corpus['data'], {url..., scrapped..}

#pandaframe

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

#TODO 1 - Label data - done
#TODO - Create Argument to Start Export data for labeling
#TODO 2 - TD IDF TO ISOLATE COVID with Linear Regression to isolate COVID - Labeled data
#TODO 3 - TD IDF TO GET TERMS OUT PER DOCUMENT LDA vs TD IDF/LSA - as labeling more important than clustering
#TODO 3 - TD IDF TO GET TERMS OUT PER DOCUMENT Then clusterin
#TODO 4 - CREATE TOPICS PER TERMS - ONE FILE PER TOPIC
#TODO 5 - SIMILARITIES, WORDS2VEC TO LIMIT ENTRIES PER TOPIC
#TODO 6 - GENERATE AIML

