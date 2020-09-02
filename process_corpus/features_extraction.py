from process_corpus.utilities import normalize_corpus
from nltk.corpus import wordnet as wn
from pathlib import Path
from xml.etree import cElementTree as ET
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from process_corpus.topics_associated_weights import topics_associated_weights
from sklearn import svm
from sklearn.cluster import KMeans
import pandas as pd
import nltk

class FeatureExtraction():

    def __init__(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "../data_saved/teaching_data.xml").resolve()

        file = open(file_path, 'r')

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

    def _trainModelLogRegr(self):

        self.data_x = normalize_corpus(self.data_x)

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
        #define vectorizer parameters
        self.tfidf_vectorizer_log_reg = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.3,
                                         use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        #train data
        X_train_tfidf = self.tfidf_vectorizer_log_reg.fit_transform(X_train) #fit the vectorizer to synopses



        #test data
        X_test_tfidf = self.tfidf_vectorizer_log_reg.transform(X_test)

        #linear regression
        self.clf_tfidf_log_reg = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                                 multi_class='multinomial', n_jobs=-1, random_state=40)

        #take train data and labels
        self.clf_tfidf_log_reg.fit(X_train_tfidf, y_train)

        #predict from list of corpus
        y_predicted_tfidf = self.clf_tfidf_log_reg.predict(X_test_tfidf)

        print(y_predicted_tfidf)

        accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = self.get_metrics(y_test, y_predicted_tfidf)
        print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                               recall_tfidf, f1_tfidf))

    def _trainModelSVC(self):

        self.data_x = normalize_corpus(self.data_x)

        X_train, X_test, y_train, y_test = train_test_split(self.data_x, self.labels_y, test_size=0.1, random_state=42)

        #define vectorizer parameters
        self.tfidf_vectorizer_svm = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.3,
                                         use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        #train data
        X_train_tfidf = self.tfidf_vectorizer_svm.fit_transform(X_train) #fit the vectorizer to synopses



        #test data
        X_test_tfidf = self.tfidf_vectorizer_svm.transform(X_test)


        self.clf_tfidf_svm = svm.SVC()

        self.clf_tfidf_svm.fit(X_train_tfidf, y_train)



        y_predicted_tfidf = self.clf_tfidf_svm.predict(X_test_tfidf)

        print(y_predicted_tfidf)

        accuracy_tfidf, precision_tfidf, recall_tfidf, f1_tfidf = self.get_metrics(y_test, y_predicted_tfidf)
        print("accuracy = %.3f, precision = %.3f, recall = %.3f, f1 = %.3f" % (accuracy_tfidf, precision_tfidf,
                                                                               recall_tfidf, f1_tfidf))

    def train_models(self):
        _trainModelSVC()
        _trainModelLogRegr()

    def useModel(self, corpus, model):

        print(corpus)
        if model == "svm" :
            X_test_tfidf = self.tfidf_vectorizer_svm.transform(normalize_corpus(corpus["data"]))
            y_predicted_tfidf = self.clf_tfidf_svm.predict(X_test_tfidf)
        else:
            X_test_tfidf = self.tfidf_vectorizer_log_reg.transform(normalize_corpus(corpus["data"]))
            y_predicted_tfidf = self.clf_tfidf_log_reg.predict(X_test_tfidf)

        new_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for idx, value in enumerate(y_predicted_tfidf):
            if value == "covid":
                new_corpus['url'].append(corpus['url'][idx])
                new_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
                new_corpus['published_date'].append(corpus['published_date'][idx])
                new_corpus['data'].append(corpus["data"][idx])


        return new_corpus




    def featureExtraction(self, corpusData):


        tfidf_matrix = TfidfVectorizer(use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1, 2))

        normalized_corpus_data = normalize_corpus(corpusData)

        matrix = tfidf_matrix.fit_transform(normalized_corpus_data)

        #svd = TruncatedSVD(n_components=10)
        #svdMatrix = svd.fit_transform(matrix)

        terms = tfidf_matrix.get_feature_names()

        totalvocab_stemmed = []
        for i in normalized_corpus_data:
            totalvocab_stemmed.extend(nltk.word_tokenize(i))

        vocab_frame = pd.DataFrame({'words': totalvocab_stemmed}, index=totalvocab_stemmed)

        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        num_clusters = 18

        km = KMeans(n_clusters=num_clusters)

        km.fit(matrix)

        #km.fit(svdMatrix)

        clusters = km.labels_.tolist()

        #cluster analysis


        # sort cluster centers by proximity to centroid
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        #linear progression
        #weight*1/x
        #matching words



        #### JUST CHANGED DATA STRUCTURE.

        occurencesMapping = [[0 for y in range(num_clusters)] for x in range(len(topics_associated_weights))]
        for idxTop, topic in enumerate(topics_associated_weights):
            print(topic, idxTop)

            for i in range(num_clusters):
                print("Cluster %d words:" % i, end='')

                for idx, ind in enumerate(order_centroids[i, :40]):  # 40 words per cluster
                    term = vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0]
                    for wordEntry in topic["values"]:
                        if((len(wn.synsets(wordEntry["word"])) and term in wn.synsets(wordEntry["word"])[0].lemma_names()) or term == wordEntry["word"]):
                            occurencesMapping[idxTop][i] += (wordEntry["weight"] * ((40-idx)/40.)) #linear progression



        mapping = [None for x in range(num_clusters)]
        print(occurencesMapping)

        for idx in range(len(occurencesMapping)):
            mapping[occurencesMapping[idx].index(max(occurencesMapping[idx]))] = topics_associated_weights[idx]["name"]

        print(mapping)
        return {"clusters": clusters, "topic_mapping": mapping}
