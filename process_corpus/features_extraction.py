import nltk
nltk.download('wordnet', quiet=True)
from nltk.corpus import wordnet as wn
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
        On entraîne le modèle de regression logistique
    '''
    def _train_model_log_regr(self, X_train_tfidf, X_test_tfidf, y_train, y_test):

        # Grâce à scikit, on déclare le modèle
        self.clf_tfidf_log_reg = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                                 multi_class='multinomial', n_jobs=-1, random_state=40)

        # Prend le corpus d'entraînement
        self.clf_tfidf_log_reg.fit(X_train_tfidf, y_train)

        # On prédit le corpus test
        y_predicted_tfidf = self.clf_tfidf_log_reg.predict(X_test_tfidf)

        print("Accuracy of the Logistic Regression model is %.3f" % accuracy_score(y_test, y_predicted_tfidf))

    '''
        On entraîne le modèle de Support Vector Machine
    '''
    def _train_model_SVM(self, X_train_tfidf, X_test_tfidf, y_train, y_test):

        # Grâce à scikit, on déclare le modèle
        self.clf_tfidf_svm = svm.SVC()

        # Prend le corpus d'entraînement
        self.clf_tfidf_svm.fit(X_train_tfidf, y_train)

        # On prédit le corpus test
        y_predicted_tfidf = self.clf_tfidf_svm.predict(X_test_tfidf)

        print("Accuracy of the SVM model is %.3f" % accuracy_score(y_test, y_predicted_tfidf))

    '''
        On entraîne les deux modèles et on les sauvegarde
    '''
    def train_models(self, file_path):

        # On vérifie que les entrées sont valides
        for idx, value in enumerate(self.data_x):
            if not value:
                print("Data missing at: ", idx)
            if not self.labels_y[idx] :
                print("Label missing at: ", idx)

        # Divise le corpus entre valeurs de test et valeurs d'entraînement (données et labels)
        X_train, X_test, y_train, y_test = train_test_split(self.data_x, self.labels_y, test_size=0.05, random_state=42)

        # Définie les paramètres du "Vectorizer". Utilise "seulement" les 200000 mots
        # les plus courant du corpus. Rejette les mots qui apparaissent dans 70% des documents
        # et retire ceux qui n'apparaissent pas d'en au moins 5% des documents
        # Utilise unigram et bigram.
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=200000,
                                         min_df=0.05, tokenizer=nltk.word_tokenize, ngram_range=(1,2))


        # Passe les données au vectorizer et crée la matrice
        X_train_tfidf = self.tfidf_vectorizer.fit_transform(X_train)


        # Calcule les vecteurs tf-idf sur les données test en utilisant la matrice précédente
        X_test_tfidf = self.tfidf_vectorizer.transform(X_test)

        # Entraîne les modèles
        self._train_model_SVM(X_train_tfidf, X_test_tfidf, y_train, y_test)
        self._train_model_log_regr(X_train_tfidf, X_test_tfidf, y_train, y_test)

        # Sauvegarde les modèles
        model = {
            "tfidf_vectorizer": self.tfidf_vectorizer,
            "clf_tfidf_svm": self.clf_tfidf_svm,
            "clf_tfidf_log_reg": self.clf_tfidf_log_reg
        }
        with open(file_path, 'wb+') as f:
            pickle.dump(model, f)
        print("Wrote models to file trained_models.pickle")

    '''
        Charge les modèles en mémoire
    '''
    def load_models(self, file_path):
        model = pickle.load(open(file_path, "rb"))
        self.tfidf_vectorizer = model["tfidf_vectorizer"]
        self.clf_tfidf_svm = model["clf_tfidf_svm"]
        self.clf_tfidf_log_reg = model["clf_tfidf_log_reg"]

        print("Loaded models from file trained_models.pickle")

    '''
        De manière conditionelle, utilise l'un ou l'autre modèle pour isoler 
        les entrées COVID.
    '''
    def use_model(self, corpus, model):
        print("1")
        # Crée les vecteurs d'entrées suivant la matrice-modèle
        X_tfidf = self.tfidf_vectorizer.transform(normalize_corpus(corpus["data"]))
        print("2")
        # On prédit en comparant les vecteurs et labels
        if model == "svm" :
            y_predicted_tfidf = self.clf_tfidf_svm.predict(X_tfidf)
        else:
            y_predicted_tfidf = self.clf_tfidf_log_reg.predict(X_tfidf)

        print("3")

        # Et on filtre le corpus pour ne garder que les entrées COVID.
        new_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for idx, value in enumerate(y_predicted_tfidf):
            if value == "covid":
                new_corpus['url'].append(corpus['url'][idx])
                new_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
                new_corpus['published_date'].append(corpus['published_date'][idx])
                new_corpus['data'].append(corpus["data"][idx])

        print("4")
        return new_corpus


    '''
        Clusterise les entrées COVID en 18 clusters, identifie les clusters
        avec des thèmes spécifiques grâce à une fonction linéaire qui dépend du poids des
        mots définissant un thème, voir TOPICS_ASSOCIATED_BY_WEIGHTS, et de l'ordre
        d'apparition du mot dans le cluster.
        On définit les clusters par k-means sur des vecteurs créés par tf-idf. 
    '''
    def feature_extraction(self, corpus_data):

        # Définit les paramètres pour la création de la matrice
        tfidf_matrix = TfidfVectorizer(tokenizer=nltk.word_tokenize, ngram_range=(1, 3))

        # Normalise le corpus (lemma, stopwords, etc...)
        normalized_corpus_data = normalize_corpus(corpus_data)

        # Crée la matrice
        matrix = tfidf_matrix.fit_transform(normalized_corpus_data)

        # Récupère tous les termes de la matrice
        terms = tfidf_matrix.get_feature_names()

        # Définit le nombre de clusters qu'on cherche à isoler
        # 18 est choisi de manière heuristique. Cela permet d'avoir des
        # clusters qui couvrent tous les thèmes et aussi une base de savoir
        # qui ne répond à aucun thème assez large pour le bot.
        number_of_clusters = 18

        # Grâce à scikit, on utilise K-means
        km = KMeans(n_clusters=number_of_clusters)

        # Puis on passe la matrice tf-idf à l'algorithme
        km.fit(matrix)

        # Et on labelise chaque vecteur (document) par son index de cluster.
        clusters = km.labels_.tolist()

        # Range feature par proximité au centroid
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        # Initialise la liste des occurences des mots-thèmes
        occurences_mapping = [[0 for y in range(number_of_clusters)] for x in range(len(TOPICS_ASSOCIATED_BY_WEIGHTS))]
        # Pour chaque thème
        for idx_topic, topic in enumerate(TOPICS_ASSOCIATED_BY_WEIGHTS):
            # Pour chaque cluster
            for i in range(number_of_clusters):
                # Pour les 40 premiers mots du cluster
                for idx, ind in enumerate(order_centroids[i, :40]):  # 40 words per cluster
                    term = terms[ind]
                    # Pour chaque mot correspondant au thème
                    for word_entry in topic["values"]:
                        # Si le mot est le même que le mot du thème
                        if (term == word_entry["word"] # Ou synonyme (après lemmatisation)
                                or (len(wn.synsets(word_entry["word"]))
                                    and term in wn.synsets(word_entry["word"])[0].lemma_names())):
                            # On calcule son poids qui dépend d'une regression linéaire lié au poids du mot-thème
                            # et de la proximité du mot au centroid du cluster
                            occurences_mapping[idx_topic][i] += (word_entry["weight"] * ((40-idx)/40.)) #linear progression


        # Initialise une liste de la taille du nombre de clusters qui indiquera par
        # index quels clusters appartiennent à quel thème
        mapping = [None for x in range(number_of_clusters)]

        # Pour chaque thème, on regarde quel est la valeur dominante sur tous les clusters
        # Et on définit ce cluster représentant le mieux le thème. La liste mapping
        # contient par index le thème de chaque cluster.
        for idx in range(len(occurences_mapping)):
            mapping[occurences_mapping[idx].index(max(occurences_mapping[idx]))] = TOPICS_ASSOCIATED_BY_WEIGHTS[idx]["name"]

        # On sort avec clusters représentant tous les documents avec l'index du cluster
        # et topic_mapping, l'index du cluster correspondant à un thème.
        return {"clusters": clusters, "topic_mapping": mapping}