from process_corpus.utilities import ManipulateCorpus
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


    def useModel(self, segment):
        corpusManipulation = ManipulateCorpus()

        X_test_tfidf = self.tfidf_vectorizer.transform(corpusManipulation.normalize_corpus(segment))

        y_predicted_tfidf = self.clf_tfidf.predict(X_test_tfidf)
        return [segment[idx] for idx,value in enumerate(y_predicted_tfidf) if value == "covid"]




    def featureExtraction(self, flattenedCorpus):

        corpusManipulation = ManipulateCorpus()

        print(len(flattenedCorpus))
        print(corpusManipulation.normalize_corpus(flattenedCorpus))
        tfidfMatrix = TfidfVectorizer(max_df=0.7, max_features=200000,
                                           min_df=0.3,
                                           use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1, 2))

        matrix = tfidfMatrix.fit_transform(corpusManipulation.normalize_corpus(flattenedCorpus))

        #svd = TruncatedSVD(n_components=10)
        #svdMatrix = svd.fit_transform(matrix)

        terms = tfidfMatrix.get_feature_names()

        totalvocab_stemmed = []
        for i in corpusManipulation.normalize_corpus(flattenedCorpus):
            totalvocab_stemmed.extend(nltk.word_tokenize(i))

        vocab_frame = pd.DataFrame({'words': totalvocab_stemmed}, index=totalvocab_stemmed)

        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        num_clusters = 12

        km = KMeans(n_clusters=num_clusters)

        km.fit(matrix)

        #km.fit(svdMatrix)

        clusters = km.labels_.tolist()

        frame = pd.DataFrame(flattenedCorpus, index=[clusters], columns=['cluster'])

        print(clusters)

        print("Top terms per cluster:")
        print()
        # sort cluster centers by proximity to centroid
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        for i in range(num_clusters):
            print("Cluster %d words:" % i, end='')

            for ind in order_centroids[i, :40]:  # replace 6 with n words per cluster
                print(' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'),
                      end=',')
            print()  # add whitespace
            print()  # add whitespace

        print()
        print()