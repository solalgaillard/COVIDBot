import spacy
#import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pickle
nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
from ManipulateCorpus.CorpusManipulation import manipulate_corpus
from ManipulateCorpus.SegmentDocuments import segmentDocuments
from ManipulateCorpus.SolveCoreferences import solveCoreference
from sklearn.model_selection import train_test_split
from pathlib import Path
from xml.etree import cElementTree as ET
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import collections

corpusManipulation = manipulate_corpus()

base_path = Path(__file__).parent



file_path = (base_path / "../data/scrapped-data-binary.pickle").resolve()
corpus = pickle.load(open(file_path, "rb" ))
print(len(corpus['data']))
print(corpus)
corpus = corpusManipulation.removeDuplicatesInCorpus(corpus)
print(corpus)
corpus['data'] = corpusManipulation.removeOverUsedSentencesFromCorpus(corpus['data'])
corpusManipulation.exportScrappedDataToFile(corpus)


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


truc()
print("test")

file_path2 = (base_path / "../data/learning-data.xml").resolve()

file = open(file_path2, 'r')


xml = file.read()
root = ET.fromstring(xml)
file.close()
data_x = []
labels_y = []
for page in list(root):
    data = page.find('data').text
    label = page.find('label').text
    data_x.append(data)
    labels_y.append(label)



'''
1 - Label data


'''
#TODO 1 - Label data - done
#TODO - Create Argument to Start Export data for labeling
#TODO 2 - TD IDF TO ISOLATE COVID with Linear Regression to isolate COVID - Labeled data
#TODO 3 - TD IDF TO GET TERMS OUT PER DOCUMENT LDA vs TD IDF/LSA - as labeling more important than clustering
#TODO 3 - TD IDF TO GET TERMS OUT PER DOCUMENT Then clusterin
#TODO 4 - CREATE TOPICS PER TERMS - ONE FILE PER TOPIC
#TODO 5 - SIMILARITIES, WORDS2VEC TO LIMIT ENTRIES PER TOPIC
#TODO 6 - GENERATE AIML

data_x = corpusManipulation.normalize_corpus(data_x)


X_train, X_test, y_train, y_test = train_test_split(data_x, labels_y, test_size=0.1, random_state=42)
#X_train, X_test, y_train, y_test = train_test_split(corpus['data'], list_labels, test_size=0.2,

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=200000,
                                 min_df=0.3,
                                 use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


#train data
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train) #fit the vectorizer to synopses



#test data
X_test_tfidf = tfidf_vectorizer.transform(X_test)

#linear regression
clf_tfidf = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                         multi_class='multinomial', n_jobs=-1, random_state=40)

#take train data and labels
clf_tfidf.fit(X_train_tfidf, y_train)

#predict from list of corpus
y_predicted_tfidf = clf_tfidf.predict(X_test_tfidf)

accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = get_metrics(y_test, y_predicted_tfidf)
print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                       recall_tfidf, f1_tfidf))
clf = svm.SVC()

clf.fit(X_train_tfidf, y_train)

y_predicted = clf.predict(X_test_tfidf)


accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = get_metrics(y_test, y_predicted)
print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                       recall_tfidf, f1_tfidf))
'''



svd = TruncatedSVD(n_components = 100)
svdMatrix = svd.fit_transform(tfidfMatrix)


terms = tfidf_vectorizer.get_feature_names()
To test within cluster, once established

X_test_tfidf = tfidf_vectorizer.transform(X_test)
clf_tfidf = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                         multi_class='multinomial', n_jobs=-1, random_state=40)
clf_tfidf.fit(X_train_tfidf)

y_predicted_tfidf = clf_tfidf.predict(X_test_tfidf)



totalvocab_stemmed = []
for i in normalizedCorpus:
    totalvocab_stemmed.extend(tokenize(i))

vocab_frame = pd.DataFrame({'words': totalvocab_stemmed}, index = totalvocab_stemmed)

print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')



num_clusters = 12

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()


docs = { 'url': corpus['url'], 'data': corpus['data'], 'cluster': clusters}
frame = pd.DataFrame(corpus, index = [clusters] , columns = ['url', 'cluster'])

print(clusters)

print("Top terms per cluster:")
print()
# sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')

    for ind in order_centroids[i, :12]:  # replace 6 with n words per cluster
        print(' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print()  # add whitespace
    print()  # add whitespace

    print("Cluster %d url:" % i, end='')
    for title in frame.loc[i]['url'].values.tolist():
        print(' %s,' % title, end='')
    print()  # add whitespace
    print()  # add whitespace

print()
print()
'''