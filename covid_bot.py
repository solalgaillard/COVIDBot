#!/usr/bin/env python3
import aiml
from export_to_aiml.export_to_aiml import export_to_aiml
import getopt
from pathlib import Path
import pickle
import sys
from process_corpus.features_extraction import FeatureExtraction
from process_corpus.segment_documents_textsplit import segment_documents_textsplit
from process_corpus.solve_coreferences_neuralcoref import solve_coreferences_neuralcoref
from process_corpus.utilities import *
from scrapper.spiders.covid_sources_spider import CovidSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

'''
    Fonction pilote qui prend les arguments de la ligne de commande en paramètres.
    La logique est d'utiliser les fichiers pickle sauf si on précise que l'on veut reconstruire le modèle
    à partir d'un certain niveau (voir paramètre build).
    Par ailleurs, si un fichier est absent, on recommence nécessairement à la reconstruction au niveau du fichier
    manquant.
    Un deuxième paramètre est celui où l'on demande expressement à exporter un fichier pour labeliser les entrées covid.
    Enfin le dernier paramètre permet de décider un classificateur par régression logistic ou par SVM.
'''
def main(labeling, build, model):
    base_path = Path(__file__).parent
    file_path = (base_path / "data_saved/scrap.pickle").resolve()

    # Scrapper
    if build in ["all", "scrap"] or not file_path.is_file():
        print("Scrapping process starting:")
        # Call crawler
        process = CrawlerProcess(get_project_settings())
        process.crawl(CovidSpider)
        process.start()

    # On charge quoi qu'il en soit le scrapper
    corpus = pickle.load(open(file_path, "rb"))

    file_path = (base_path / "data_saved/corefseg.pickle").resolve()

    # Résolution des coréférences et segementation du corpus
    if build in ["all", "scrap", "corefseg"] or not file_path.is_file():
        print("Segmentation and Coreference Resolution process starting:\nThis is a long process...")
        corpus = remove_all_specific_substrings(remove_overused_sentences_from_corpus(remove_duplicates_in_corpus(corpus)))

        tmp_corpus_data = []
        for idx, document in enumerate(corpus['data']):
            tmp_corpus_data.append([])
            for segment in segment_documents_textsplit(document):
                tmp_corpus_data[idx].append(segment)
                #tmp_corpus_data[idx].append(solve_coreferences_neuralcoref(segment))

        corpus['data'] = tmp_corpus_data

        with open(file_path, 'wb+') as f:
            pickle.dump(corpus, f)
        print("Wrote to file corefseg.pickle")
    else:
        print("Loaded corefseg.pickle")
        corpus = pickle.load(open(file_path, "rb"))

    '''
    filtered_corpus = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    for idx, data in enumerate(corpus["data"]):
        if(idx<2):
            filtered_corpus['url'].append(corpus['url'][idx])
            filtered_corpus['scrapped_date'].append(corpus['scrapped_date'][idx])
            filtered_corpus['published_date'].append(corpus['published_date'][idx])
            filtered_corpus['data'].append(data)

    #corpus = filtered_corpus
    #print(corpus)
    '''
    file_path = (base_path / "data_saved/teaching_data.xml").resolve()

    # Exporte fichier pour labélisation et sort du programme
    if labeling or not file_path.is_file():
        print("Exporting teaching_data.xml for labeling.",
              "Please review the file, label the entries and relaunch the program.")
        iteration = labeling if labeling else 500
        export_scrapped_data_to_file_for_labeling(corpus, file_path, iteration)
        return

    file_path = (base_path / "data_saved/trained_models.pickle").resolve()

    # Construit le modèle pour classifier entrées COVID et entrées non-COVID
    if build in ["all", "scrap", "corefseg", "model"] or not file_path.is_file():
        feature_extraction = FeatureExtraction((base_path / "data_saved/teaching_data.xml").resolve())
        print("Loaded teaching_data.xml\nTraining models...")
        feature_extraction.train_models(file_path)
    else:
        feature_extraction = FeatureExtraction()
        feature_extraction.load_models(file_path)
        print("Loaded trained_models.pickle")

    file_path = (base_path / "data_saved/covidentries.pickle").resolve()

    # Utilise le modèle
    if build in ["all", "scrap", "corefseg", "model", "covidentries"] or not file_path.is_file():
        print("Using models to isolate covid entries only...")
        corpus = feature_extraction.use_model(each_segment_gets_description(corpus), model)
        with open(file_path, 'wb+') as f:
            pickle.dump(corpus, f)
        print("Wrote to file covidentries.pickle")
    else:
        corpus = pickle.load(open(file_path, "rb"))
        print("Loaded covidentries.pickle")

    file_path = (base_path / "data_saved/covidtopics.pickle").resolve()

    # Clusterise par Kmeans les thèmes des entrées sur le COVID.
    if build in ["all", "scrap", "corefseg", "model", "covidentries", "covidtopics"] or not file_path.is_file():
        print("Extracting themes from corpus...")
        result_topics = feature_extraction.feature_extraction(corpus["data"])
        with open(file_path, 'wb+') as f:
            pickle.dump(result_topics, f)
        print("Wrote to file covidtopics.pickle")
    else:
        result_topics = pickle.load(open(file_path, "rb"))
        print("Loaded covidtopics.pickle")

    file_path = (base_path / "data_saved/bot_brain.brn").resolve()

    # Construit le chatbot AIML.
    kernel = aiml.Kernel()
    if build in ["all", "scrap", "corefseg", "model", "covidentries", "covidtopics", "botbrain"] \
            or not file_path.is_file():
        print("Creating bot...")
        export_to_aiml(result_topics, corpus)
        kernel.learn("./chat_bot_files/covid_bot.aiml")
        kernel.respond("load aiml files")
        kernel.saveBrain(file_path)
        print("Wrote to file bot_brain.brn")
    else:
        kernel.bootstrap(brainFile=file_path)
        print("Loaded bot_brain.brn")

    # Le charge
    while True:
        inputed = input("Enter your message >> ")
        if inputed == "quit":
            print("Bye bye")
            return
        nlp_inputed = nlp(expand_contractions(inputed))
        lemmatized_inputed = ' '.join([token.lemma_ if token.dep_ == 'ROOT' and token.pos_ == 'VERB' else token.text for token in nlp_inputed])
        res = kernel.respond(lemmatized_inputed)
        if (len(res) > 0):
            print(res)
        else:
            print('No answer in knowledge base')

# Script de début
if __name__ == "__main__":
    # Arguments par défaut.
    labeling = 0 ; build = "none" ; model = "svm" #ou log_reg
    try:
        # Retire premier argument de sys, donne options longues et courtes.
        arguments, values = getopt.getopt(sys.argv[1:], "b:l:m:", ["build=", "labeling=", "model="])

        # Parse la ligne de commande
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-b", "--build"):
                if currentValue in ["all","scrap","corefseg", "model", "covidentries", "covidtopics", "botbrain"]:
                    build = currentValue
                else:
                    print("Could not recognize the build option, starting from scratch.")

            elif currentArgument in ("-m", "--model"):
                if currentValue in ["logreg", "SVM"]:
                    model = currentValue

            elif currentArgument in ("-l", "--labeling"):
                build = "none"
                labeling = int(currentValue)

    except getopt.error as err:
        # Imprime erreur sur les arguments
        print(str(err))

    # Et lance programme
    main(labeling, build, model)




#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos that are done




#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos not done


#sudo apt install python3-pip
#sudo apt-get install python3-venv
#python3 -m venv venv
#source ./env/bin/activate
#pip3 install -r requirements.txt
#Make sure last Chrome is installed, not chromium but chrome


