import nltk
nltk.download('wordnet', quiet=True)
from nltk.corpus import wordnet as wn
import pandas as pd
import pickle
from process_corpus.topics_associated_weights import TOPICS_ASSOCIATED_BY_WEIGHTS
from process_corpus.utilities import normalize_corpus
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xml.etree import cElementTree as ET

'''
    Classe qui définit les méthodes pour créer le modèle qui permet
    d'extraire les segments qui portent sur le covid ainsi que réaliser
    des clusters autour des différents thèmes.
'''
class FeatureExtraction():

    '''
        Si les modèles entraînés ne sont pas déjà dans un fichier, on passe nos labels
        dans le constructor et le xml est parsé en prenant d'un côté le texte, de l'autre
        les labels. On normalize le corpus ensuite. C'est-à-dire, on retire les accents,
        on défait les contractions, on met le texte en miniscule, on enlève les lignes en trop,
        on lemmatise, on enlève les caractères spéciaux, les espaces blancs et les stopwords.
    '''
    def __init__(self, file_path=None):
        if file_path:
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
            self.data_x = normalize_corpus(self.data_x)

    '''
        On entraîne
    '''
    def _train_model_log_regr(self, X_train_tfidf, X_test_tfidf, y_train, y_test):

        #linear regression
        self.clf_tfidf_log_reg = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                                 multi_class='multinomial', n_jobs=-1, random_state=40)

        #take train data and labels
        self.clf_tfidf_log_reg.fit(X_train_tfidf, y_train)

        #predict from list of corpus
        y_predicted_tfidf = self.clf_tfidf_log_reg.predict(X_test_tfidf)

        print("accuracy of the model = %.3f, " % accuracy_score(y_test, y_predicted_tfidf))

    def _train_model_SVM(self, X_train_tfidf, X_test_tfidf, y_train, y_test):

        self.clf_tfidf_svm = svm.SVC()

        self.clf_tfidf_svm.fit(X_train_tfidf, y_train)

        y_predicted_tfidf = self.clf_tfidf_svm.predict(X_test_tfidf)

        print("accuracy of the model = %.3f, " % accuracy_score(y_test, y_predicted_tfidf))

    def train_models(self, file_path):

        for idx, value in enumerate(self.data_x):
            if not value:
                print("Data missing at: ", idx)
            if not self.labels_y[idx] :
                print("Label missing at: ", idx)


        X_train, X_test, y_train, y_test = train_test_split(self.data_x, self.labels_y, test_size=0.1, random_state=42)
        #define vectorizer parameters
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.3,
                                         use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        #train data
        X_train_tfidf = self.tfidf_vectorizer.fit_transform(X_train) #fit the vectorizer to synopses


        #test data
        X_test_tfidf = self.tfidf_vectorizer.transform(X_test)

        self._train_model_SVM(X_train_tfidf, X_test_tfidf, y_train, y_test)
        self._train_model_log_regr(X_train_tfidf, X_test_tfidf, y_train, y_test)
        #SAVE TO FILE THE MODELS
        model = {
            "tfidf_vectorizer": self.tfidf_vectorizer,
            "clf_tfidf_svm": self.clf_tfidf_svm,
            "clf_tfidf_log_reg": self.clf_tfidf_log_reg
        }
        with open(file_path, 'wb+') as f:
            pickle.dump(model, f)
        print("Wrote models to file trained_models.pickle")

    def load_models(self, file_path):
        model = pickle.load(open(file_path, "rb"))
        self.tfidf_vectorizer_svm = model["tfidf_vectorizer_svm"]
        self.clf_tfidf_svm = model["clf_tfidf_svm"]
        self.tfidf_vectorizer_log_reg = model["tfidf_vectorizer_log_reg"]
        self.clf_tfidf_log_reg = model["clf_tfidf_log_reg"]

        print("Loaded models from file trained_models.pickle")


    def use_model(self, corpus, model):

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




    def feature_extraction(self, corpus_data):

        tfidf_matrix = TfidfVectorizer(use_idf=True, tokenizer=nltk.word_tokenize, ngram_range=(1, 2))

        normalized_corpus_data = normalize_corpus(corpus_data)

        matrix = tfidf_matrix.fit_transform(normalized_corpus_data)

        terms = tfidf_matrix.get_feature_names()

        total_vocab_normalized = []
        for i in normalized_corpus_data:
            total_vocab_normalized.extend(nltk.word_tokenize(i))

        vocab_frame = pd.DataFrame({'words': total_vocab_normalized}, index=total_vocab_normalized)
        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        number_of_clusters = 18

        km = KMeans(n_clusters=number_of_clusters)

        km.fit(matrix)

        clusters = km.labels_.tolist()

        #cluster analysis


        # sort cluster centers by proximity to centroid
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        #linear progression
        #weight*1/x
        #matching words


        occurences_mapping = [[0 for y in range(number_of_clusters)] for x in range(len(TOPICS_ASSOCIATED_BY_WEIGHTS))]
        for idx_topic, topic in enumerate(TOPICS_ASSOCIATED_BY_WEIGHTS):

            for i in range(number_of_clusters):
                for idx, ind in enumerate(order_centroids[i, :40]):  # 40 words per cluster
                    term = vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0]
                    for word_entry in topic["values"]:
                        if((len(wn.synsets(word_entry["word"])) and term in wn.synsets(word_entry["word"])[0].lemma_names()) or term == word_entry["word"]):
                            occurences_mapping[idx_topic][i] += (word_entry["weight"] * ((40-idx)/40.)) #linear progression



        mapping = [None for x in range(number_of_clusters)]
        print(occurences_mapping)

        for idx in range(len(occurences_mapping)):
            mapping[occurences_mapping[idx].index(max(occurences_mapping[idx]))] = TOPICS_ASSOCIATED_BY_WEIGHTS[idx]["name"]

        print(mapping)
        return {"clusters": clusters, "topic_mapping": mapping}
