#!/usr/bin/env python3

import sys
import scrapy
from scrapy.crawler import CrawlerProcess


def main():
    print("Hello World!")

if __name__ == "__main__":
    # total arguments
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hmo:"

    # Long options
    long_options = ["Help", "My_file", "Output ="]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print("Diplaying Help")

            elif currentArgument in ("-m", "--My_file"):
                print("Displaying file_name:", sys.argv[0])

            elif currentArgument in ("-o", "--Output"):
                print(("Enabling special output mode (% s)") % (currentValue))

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    main()




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

    #TODO - Add Random To centralize cue and Entities pattern as shown below - done
    #TODO - Better way to find patterns(single nouns and no verbs?) - done
    #TODO - Bring permutations within one loop and test code - done

'''
    <template>
        <random>
           <li> Hello! </li>
           <li> Hi! Nice to meet you! </li>
        </random>
     </template>
'''


#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos not done


    #TODO - PIPE NLP

    #TODO - Change Folder name of export_to_aiml, this is causing the issue

    #TODO 6 - Refactor all the code
        #TODO 6 - a - Prepare proper packaging
        #TODO 6 - b - On Scrapper, writing to files need to be invoked only once
        #TODO 6 - c - Paths must be resolved properly
        #TODO 6 - d - Bring in Pandas DataFrame

    #TODO - CLEAR AIML FILES ON WRITE

    #TODO 7 - Allow parameters to be passed to cmd line to isolate the different type of actions possible
        #TODO 7 - a - Scrap only the web
        #TODO 7 - b - Export Data for labelling
        #TODO 7 - c - Load
        #TODO 7 - c - Pass type model to recognize covid text
        #TODO 7 - c - save model
        #TODO 7 - c - load model
        #TODO 7 - c - generate aiml
        #TODO 7 - c - launch bot
        #TODO 7 - c - start-from-scratch

    #TODO 8 - Make sure it can be deployed and built anywhere.
        #TODO 8 - a - Check all Packages
        #TODO 8 - b - Check Environment - Envpath
        #TODO 8 - c - Install locally webdriver / Check that the path works

    #TODO 9 - Save Brain of Chatbot
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