from process_corpus.utilities import ManipulateCorpus
from nltk.corpus import wordnet as wn
from pathlib import Path
from xml.etree import cElementTree as ET
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import collections
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import svm
from sklearn.cluster import KMeans
import pandas as pd
import nltk

class featureExtractions():

    def __init__(self):
        base_path = Path(__file__).parent
        file_path2 = (base_path / "../data/learning-data.xml").resolve()

        file = open(file_path2, 'r')

        xml = file.read()
        root = ET.fromstring(xml)
        file.close()
        self.data_x = []
        self.labels_y = []
        for doc in list(root):
            for data in doc.findall("data"):
                segment = data.find('segment').text
                label = data.find('label').text
                self.data_x.append(segment)
                self.labels_y.append(label)

    def get_metrics(self, y_test, y_predicted):
        # true positives / (true positives+false positives)
        precision = precision_score(y_test, y_predicted, pos_label=None,
                                    average='weighted')
        # true positives / (true positives + false negatives)
        recall = recall_score(y_test, y_predicted, pos_label=None,
                              average='weighted')

        # harmonic mean of precision and recall
        f1 = f1_score(y_test, y_predicted, pos_label=None, average='weighted')

        # true positives + true negatives/ total0
        accuracy = accuracy_score(y_test, y_predicted)
        return accuracy, precision, recall, f1

    def trainModelLogRegr(self):

        corpusManipulation = ManipulateCorpus()

        self.data_x = corpusManipulation.normalize_corpus(self.data_x)

        print(self.data_x)
        print(len(self.data_x))

        for idx, value in enumerate(self.data_x):
            if(not value):
                print("error", idx)

        print("chiche")
        for idx, value in enumerate(self.labels_y):
            if(not value):
                print("error", idx)


        X_train, X_test, y_train, y_test = train_test_split(self.data_x, self.labels_y, test_size=0.1, random_state=42)
        #X_train, X_test, y_train, y_test = train_test_split(corpus['data'], list_labels, test_size=0.2,
        #define vectorizer parameters
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.3,
                                         use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        #train data
        X_train_tfidf = self.tfidf_vectorizer.fit_transform(X_train) #fit the vectorizer to synopses



        #test data
        X_test_tfidf = self.tfidf_vectorizer.transform(X_test)

        #linear regression
        self.clf_tfidf = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                                 multi_class='multinomial', n_jobs=-1, random_state=40)

        #take train data and labels
        self.clf_tfidf.fit(X_train_tfidf, y_train)

        #predict from list of corpus
        y_predicted_tfidf = self.clf_tfidf.predict(X_test_tfidf)

        print(y_predicted_tfidf)

        accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = self.get_metrics(y_test, y_predicted_tfidf)
        print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                               recall_tfidf, f1_tfidf))

    def trainModelSVC(self):

        corpusManipulation = ManipulateCorpus()

        self.data_x = corpusManipulation.normalize_corpus(self.data_x)

        X_train, X_test, y_train, y_test = train_test_split(self.data_x, self.labels_y, test_size=0.1, random_state=42)
        #X_train, X_test, y_train, y_test = train_test_split(corpus['data'], list_labels, test_size=0.2,
        #define vectorizer parameters
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.3,
                                         use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        #train data
        X_train_tfidf = self.tfidf_vectorizer.fit_transform(X_train) #fit the vectorizer to synopses



        #test data
        X_test_tfidf = self.tfidf_vectorizer.transform(X_test)


        self.clf_tfidf = svm.SVC()

        self.clf_tfidf.fit(X_train_tfidf, y_train)



        y_predicted_tfidf = self.clf_tfidf.predict(X_test_tfidf)

        print(y_predicted_tfidf)

        accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = self.get_metrics(y_test, y_predicted_tfidf)
        print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                               recall_tfidf, f1_tfidf))


    def useModel(self, corpus):
        corpusManipulation = ManipulateCorpus()

        print(corpus)
        X_test_tfidf = self.tfidf_vectorizer.transform(corpusManipulation.normalize_corpus(corpus["data"]))

        y_predicted_tfidf = self.clf_tfidf.predict(X_test_tfidf)

        newCorpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for idx, value in enumerate(y_predicted_tfidf):
            if value == "covid":
                newCorpus['url'].append(corpus['url'][idx])
                newCorpus['scrapped_date'].append(corpus['scrapped_date'][idx])
                newCorpus['published_date'].append(corpus['published_date'][idx])
                newCorpus['data'].append(corpus["data"][idx])


        return newCorpus




    def featureExtraction(self, corpusData):

        corpusManipulation = ManipulateCorpus()

        print(corpusManipulation.normalize_corpus(corpusData))
        tfidfMatrix = TfidfVectorizer(use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1, 2))

        matrix = tfidfMatrix.fit_transform(corpusManipulation.normalize_corpus(corpusData))

        #svd = TruncatedSVD(n_components=10)
        #svdMatrix = svd.fit_transform(matrix)

        terms = tfidfMatrix.get_feature_names()

        totalvocab_stemmed = []
        for i in corpusManipulation.normalize_corpus(corpusData):
            totalvocab_stemmed.extend(nltk.word_tokenize(i))

        vocab_frame = pd.DataFrame({'words': totalvocab_stemmed}, index=totalvocab_stemmed)

        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        num_clusters = 16

        km = KMeans(n_clusters=num_clusters)

        km.fit(matrix)

        #km.fit(svdMatrix)

        clusters = km.labels_.tolist()

        #cluster analysis


        print(clusters)

        print("Top terms per cluster:")
        print()
        # sort cluster centers by proximity to centroid
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        #linear progression
        #weight*1/x
        #matching words

        topics = {
            "symptom": [
                    {"word": "symptom", "weight": 1},
                    {"word": "respiratory", "weight": 1},
                    {"word": "tract", "weight": 1},
                    {"word": "severe", "weight": 1},
                    {"word": "stool", "weight": .6},
                    {"word": "laboratory", "weight": .4},
                ],
            "test": [
                    {"word": "test", "weight": 1},
                    {"word": "laboratory", "weight": 1},
                    {"word": "precaution", "weight": .5},
                    {"word": "cdc", "weight": .5},
                    {"word": "processing", "weight": .8},
                    {"word": "guidance", "weight": .3},
                    {"word": "specimen", "weight": .8},
                    {"word": "guideline", "weight": .3},
                    {"word": "infectious", "weight": .1},
                    {"word": "processing", "weight": .8},
                    {"word": "detectable", "weight": .7},
                ],
            "data": [
                    {"word": "number", "weight": 1},
                    {"word": "death", "weight": 1},
                    {"word": "case", "weight": 1},
                    {"word": "country", "weight": .5},
                    {"word": "record", "weight": 1},
                    {"word": "figure", "weight": 1},
                    {"word": "rate", "weight": 1},
                    {"word": "total", "weight": 1},
                    {"word": "toll", "weight": 1},
                    {"word": "percentage", "weight": .8},
                ],
            "vaccine/treatment": [
                    {"word": "vaccine", "weight": 1},
                    {"word": "trial", "weight": 1},
                    {"word": "drug", "weight": .6},
                    {"word": "immune", "weight": .7},
                    {"word": "treatment", "weight": .6},
                    {"word": "antibody", "weight": .5},
                ],

            "material/healthcare": [
                    {"word": "respirator", "weight": 1},
                    {"word": "patient", "weight": 1},
                    {"word": "n95", "weight": 1},
                    {"word": "procedure", "weight": .7},
                    {"word": "protection", "weight": .7},
                ],

            "travel/flights/airline": [
                    {"word": "travel", "weight": 1},
                    {"word": "transportation", "weight": 1},
                    {"word": "flight", "weight": 1},
                    {"word": "cruise", "weight": 1},
                    {"word": "crew", "weight": 1},
                    {"word": "traveler", "weight": 1},
                    {"word": "airline", "weight": 1},
                    {"word": "entry", "weight": 1},
                    {"word": "disembarkation", "weight": 1},
                ],
            "politics": [
                    {"word": "government", "weight": .7},
                    {"word": "trump", "weight": 1},
                    {"word": "european", "weight": .8},
                    {"word": "leader", "weight": .5},
                    {"word": "us", "weight": .4},
                    {"word": "senate", "weight": 1},
                    {"word": "briefing", "weight": 1},
                    {"word": "official", "weight": .5},
                    {"word": "eu", "weight": .4},
                    {"word": "republican", "weight": 1},
                    {"word": "lockdown", "weight": .3},
                    {"word": "public", "weight": .3},
                    {"word": "mask", "weight": .2},
                    {"word": "country", "weight": .2},
                ]
        } #contain

        occurencesMapping = {}
        for topic in topics:
            occurencesMapping[topic] = [0 for x in range(num_clusters)]
            for i in range(num_clusters):
                print("Cluster %d words:" % i, end='')

                for idx,ind in enumerate(order_centroids[i, :40]):  # replace 6 with n words per cluster
                    term = vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0]
                    for wordEntry in topics[topic]:
                        if((len(wn.synsets(wordEntry["word"])) and term in wn.synsets(wordEntry["word"])[0].lemma_names()) or term == wordEntry["word"]):
                            print(ind)
                            print(((40-ind)/40.), wordEntry["weight"])
                            occurencesMapping[topic][i] += (wordEntry["weight"] * ((40-idx)/40.)) #linear progression

                    #wn.synsets('change')[0].lemma_names()

                    print(' %s' % term, end=',')
                print()  # add whitespace
                print()  # add whitespace

            print()
            print()

        print(topics)

        mapping = [None for x in range(num_clusters)]
        print(occurencesMapping)
        for topic in occurencesMapping:
            occurencesMapping[topic] = occurencesMapping[topic].index(max(occurencesMapping[topic]))
            mapping[occurencesMapping[topic]] = topic

        print(mapping)
        return {"clusters": clusters, "topic_mapping": mapping}