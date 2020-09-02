#!/usr/bin/env python3

import sys
import getopt
import pickle
from process_corpus.utilities import *
from process_corpus.segment_documents_textsplit import segment_documents_textsplit
from process_corpus.solve_coreferences_neuralcoref import solve_coreferences_neuralcoref
from process_corpus.features_extraction import FeatureExtraction
from export_to_aiml.export_to_aiml import export_to_aiml
from pathlib import Path
import aiml
import scrapy
from scrapper.spiders.covid_sources_spider import CovidSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


def main(labeling, build, model):
    base_path = Path(__file__).parent
    file_path = (base_path / "data_saved/scrap.pickle").resolve()

    if build in ["all", "scrap"] or not file_path.is_file():
        process = CrawlerProcess(get_project_settings())
        process.crawl(CovidSpider)
        process.start()

    corpus = pickle.load(open(file_path, "rb"))

    print(corpus)

    file_path = (base_path / "data_saved/corefseg.pickle").resolve()

    if build in ["all", "scrap", "corefseg"] or not file_path.is_file():
        corpus = remove_duplicates_in_corpus(corpus)
        corpus['data'] = [segment_documents_textsplit(solve_coreferences_neuralcoref(document)) for document in
                          corpus['data']]
        with open(file_path, 'wb+') as f:
            pickle.dump(corpus, f)
        print("Wrote to file corefseg.pickle")
    else:
        corpus = pickle.load(open(file_path, "rb"))


    file_path = (base_path / "data_saved/teaching_data.xml").resolve()

    if labeling or not file_path.is_file():
        print("LABELING")
        export_scrapped_data_to_file_for_labeling(corpus)
        return

    file_path = (base_path / "data_saved/trained_models.xml").resolve()

    #if build not in ["all", "scrap", "corefseg", "model"] or not file_path.isfile():
    #PASS TEACHING FILE, IF NO TEACHING FILE, FOR


    feature_extraction = FeatureExtraction()

    #TRAIN BOTH MODELS & SAVE
    feature_extraction.trainModelSVC()




    file_path = (base_path / "data_saved/covidentries.pickle").resolve()

    if build in ["all", "scrap", "corefseg", "model", "covidentries"] or not file_path.is_file():
        corpus = feature_extraction.useModel(each_segement_gets_description(corpus), model)
        with open(file_path, 'wb+') as f:
            pickle.dump(corpus, f)
        print("Wrote to file covidentries.pickle")
    else:
        corpus = pickle.load(open(file_path, "rb"))


    file_path = (base_path / "data_saved/covidtopics.pickle").resolve()

    if build in ["all", "scrap", "corefseg", "model", "covidentries", "covidtopics"] or not file_path.is_file():
        result_topics = feature_extraction.featureExtraction(corpus["data"])
        with open(file_path, 'wb+') as f:
            pickle.dump(result_topics, f)
        print("Wrote to file covidtopics.pickle")
    else:
        result_topics = pickle.load(open(file_path, "rb"))



    file_path = (base_path / "data_saved/bot_brain.brn").resolve()

    kernel = aiml.Kernel()
    if build in ["all", "scrap", "corefseg", "model", "covidentries", "covidtopics", "botbrain"] or not file_path.is_file():
        export_to_aiml(result_topics)
        kernel.learn("./chat_bot/covid_bot.aiml")
        kernel.respond("load aiml files")
        kernel.saveBrain("bot_brain.brn")
    else:
        kernel.bootstrap(brainFile=file_path)
        print("Wrote to file bot_brain.brn")

    while True:
        inputed = input("Enter your message >> ")
        res = kernel.respond(inputed)
        if (len(res) > 0):
            print(res)
        else:
            print('loopiloop')


if __name__ == "__main__":
    # total arguments
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    options = ["build =", "labeling", "model"]
    labeling = False ; build = "none" ; model = "svm" #ou log_reg
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, "b:lm:", options)


        # checking each argument

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-b", "--build"):
                if currentValue in ["all","scrap","corefseg", "model", "covidentries", "covidtopics", "botbrain"]:
                    build = currentValue
                else:
                    print("Could not recognize the build option, starting from scratch.")

            elif currentArgument in ("-m", "--model"):
                if currentValue in ["logreg", "SVM"]:
                    build = currentValue

            elif currentArgument in ("-l", "--labeling"):
                build = "none"
                labeling = True


    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    main(labeling, build, model)




#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos that are done

    #TODO - Scrapper - done
        #TODO Understand why rules won't work and the filter is not applied
            # (regex preparsing relative path, not absolute) - done
        #TODO Bread-width-first (see settings file) - done
        #TODO Kill all queued requests (might not be relevant anymore since I'm not following requests) - done
        #TODO Extract date for each article - Done
        #TODO Limit scrapping to what is past three months - done

    #TODO - Coreference extraction. - done
    #TODO - Text Segmentation - done
    #TODO - Automatize to get a small corpus to label - done
    #TODO - Label data - done
    #TODO - TF-IDF with Logistic Regression or SVM to isolate COVID - Labeled data 500 - done
    #TODO - TF-IDF then K-Means clustering on all corpus to get terms out -done
    #TODO - Get topic name by the most used terms per cluster - done
    #TODO - Generate one aiml file per topic - done
    #TODO - Review structure of dictionnary for mapping
    #TODO - Understand why one topic is not in the cluster list - done
    #TODO - Add non-topics to bot - done

    #TODO - Add Random Tag To centralize cue and Entities pattern as shown below - done
    #TODO - Better way to find patterns(single nouns and no verbs?) - done
    #TODO - Bring permutations within one loop and test code - done
    #TODO 9 - Save Brain of Chatbot - done


#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos not done

    #TODO 6 - Refactor all the code
        #TODO 6 - a - Prepare proper packaging
        #TODO 6 - b - On Scrapper, writing to files need to be invoked only once
        #TODO 6 - c - Paths must be resolved properly
        #TODO 6 - d - Bring in Pandas DataFrame

    #TODO - CLEAR AIML FILES ON WRITE

    #TODO 7 - Allow parameters to be passed to cmd line to isolate the different type of actions possible
        #TODO 7 - a - Scrap only the web - d
        #TODO 7 - b - Export Data for labelling - d
        #TODO 7 - c - Load - d
        #TODO 7 - c - Pass type model to recognize covid text - d
        #TODO 7 - c - generate aiml - d
        #TODO 7 - c - launch bot - d
        #TODO 7 - c - start-from-scratch - d
        # TODO 7 - c - save model ====> DOING RIGHT NOW
        # TODO 7 - c - load model ====> DOING RIGHT NOW

    #TODO 8 - Make sure it can be deployed and built anywhere.
        #TODO 8 - a - Check all Packages
        #TODO 8 - b - Check Environment - Envpath
        #TODO 8 - c - Install locally webdriver / Check that the path works


    #TODO 10 - Develop Mecanism to flag answer when special user
        #TODO 10 - a - Need to be able to blacklist entry - put it in a file

    #TODO 11 - - Provide Basic AIML Bot
    #TODO 12 - Comment Code
    #TODO 13 - Investigate way better Scrapping
        #TODO 13 - a - Rules for automatic path to driver
        #TODO 13 - b - Make Driver Path absolute
        #TODO 13 - c - Investigate Paywall for NYT, do I need a new Login?

    #TODO 14 - Label more Data and check between Logistic Regression and SVM which one is best
    #TODO 15 - Review clustering process

#-----------------------------------------------------------------------------------------------------------------------
#Those are all the nice to have
    #TODO - PIPE NLP
    #TODO - 1 - Check if similarities between facts avec word2vec and use published date and source to decide which
            # to keep
    #TODO - 2 - Cron Job to scrap and rebuild automatically the bot
    #TODO - 3 - Unit Testing
    #TODO - 4 - Word embeddings all across would have been more efficient



"""
  for segment in corpus["data"]:
        nlp_segment = nlp(segment)
        for token in nlp_segment:
            if token.dep_ == "nsubj" and token.text.lower() not in ["who, which, what, where, how, when"]: #And not interrogative
                statements = textacy.extract.semistructured_statements(nlp_segment, token.text)

"""