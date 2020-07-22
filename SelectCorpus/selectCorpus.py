import spacy
import pickle
nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
from process_corpus.utilities import ManipulateCorpus
from process_corpus.segment_documents import SegmentDocuments
from process_corpus.solve_coreferences import solveCoreference
from process_corpus.extract_features import featureExtractions
from process_corpus.extract_facts import ExtractFacts
from pathlib import Path
import re
from functools import reduce

base_path = Path(__file__).parent
corpusManipulation = ManipulateCorpus()
solve_coreference = solveCoreference()
segment_documents = SegmentDocuments()


#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos that are done

#TODO - Coreference extraction. - done
#TODO - Text Segmentation - done
#TODO - Automatize to get a small corpus to label.
#TODO - Label data - done
    #TODO - TD IDF TO ISOLATE COVID with Logistic Regression to isolate COVID - Labeled data 500
    #TODO - TD IDF TO GET TERMS OUT PER DOCUMENT Then K-Means clustering -done
    #TODO - CREATE TOPICS PER TERMS - ONE FILE PER TOPIC - done
    #TODO - GENERATE AIML - done
#TODO EXTRACT DATE ON EACH DOMAIN - Done

#TODO UNDERSTAND WHY RULES DON't work - don't filter ? -DONE
#TODO BREAD-WIDTH FIRST - done
#TODO KILL ALL QUEUED REQUESTS - done
#TODO MAKE INSTALL LOCALLY OF DRIVER - done

#TODO LIMIT TO PAST THREE MONTHS - done

#-----------------------------------------------------------------------------------------------------------------------
#Those are all the todos not done
    #TODO 1 - Review structure of dictionnary
    #TODO 2 - Understand why one topic is not in the cluster list
    #TODO 3 - Add non-topics to bot
    #TODO 4 - Better way to find patterns(single nouns and no verbs?)
    #TODO 5 - Add Random To centralize cue and Entities pattern as shown below
'''
    <template>
        <random>
           <li> Hello! </li>
           <li> Hi! Nice to meet you! </li>
        </random>
     </template>
'''
    #TODO 6 - Refactor all the code
        #TODO 6 - a - Prepare proper packaging
        #TODO 6 - b - On Scrapper, writing to files need to be invoked only once
#       #TODO 6 - c - Bring in Pandas DataFrame

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
        #TODO 8 - b - Check Environment
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

#-----------------------------------------------------------------------------------------------------------------------
#Those are all the nice to have
    #TODO - 1 - Check if similarities between facts avec word2vec and use published date and source to decide which
# to keep
    #TODO - 2 - Cron Job
    #TODO - Unit Testing





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

def replaceXMLSpecialChar(aString):
    value_esc_char = aString.replace("&", "&amp;")
    value_esc_char = value_esc_char.replace("<", "&lt;")
    value_esc_char = value_esc_char.replace(">", "&gt;")
    value_esc_char = value_esc_char.replace('"', "&quot;")
    value_esc_char = value_esc_char.replace("'", "&apos;")
    return value_esc_char

def setTopicString(topics):
    allTopicSetters = ""

    for topic in topics:
        allPatterns = [f'* {topic.upper()} *', f'{topic.upper()} *', f'* {topic.upper()}', topic.upper()]
        for pattern in allPatterns:
            allTopicSetters += ('\n\t<category>'
                               f'\n\t\t<pattern>{replaceXMLSpecialChar(pattern)}</pattern>'
                               '\n\t\t<template>'
                               f'\n\t\t\t<think><set name = "topic">{replaceXMLSpecialChar(topics[0].upper())}</set></think>'
                               f'\n\t\t\tI know a lot about {replaceXMLSpecialChar(topic)}'
                               '\n\t\t</template>'
                               '\n\t</category>')


    return allTopicSetters

# on regrette l'absence d'aiml 2... avec le caret comme wildcard
def setAllPermutationsString(all_statements):

    allPermutations = ""

    for statement in all_statements:
        entity, cue, fact = statement
        print("* entity:", entity, ", cue:", cue, ", fact:", fact)
        template = f'{entity.text.capitalize()} {cue.text} {fact.text}.'
        allPatterns = [
            f'* {cue.text.upper()} * {entity.text.upper()} *',
            f'{cue.text.upper()} * {entity.text.upper()} *',
            f'{cue.text.upper()} {entity.text.upper()} *',
            f'* {cue.text.upper()} {entity.text.upper()}',
            f'* {cue.text.upper()} * {entity.text.upper()}',
            f'* {cue.text.upper()} {entity.text.upper()} *',
            f'{cue.text.upper()} * {entity.text.upper()}',
            f'{cue.text.upper()} {entity.text.upper()}',
        ]
        for pattern in allPatterns:
            allPermutations += ('\n\t\t<category>'
                                f'\n\t\t\t<pattern>{replaceXMLSpecialChar(pattern)}</pattern>'
                                f'\n\t\t\t<template>{replaceXMLSpecialChar(template)}</template>'
                                '\n\t\t</category>')


    return allPermutations




def createTopic(allTopics, statements):
    with open(f'./chatBot/{allTopics[0]}.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{setTopicString(allTopics)}'
                   f'\n\t<topic name = "{allTopics[0].upper()}">'
                   f'{setAllPermutationsString(statements)}'
                   '\n\t\t<category>'
                   '\n\t\t\t<pattern>*</pattern>'
                   '\n\t\t\t<template>'
                   '\n\t\t\t\t<think><set name="topic"><!-- No Topic --></set></think>'
                   '\n\t\t\t\tOk, changing topic.'
                   '\n\t\t\t</template>'
                   '\n\t\t</category>'
                   '\n\t</topic>'
                   '\n</aiml>')


def createPilotFile(allTopics):
    print(allTopics)
    with open(f'./chatBot/covid-bot.aiml', "w+", encoding="utf-8") as file:
        nl_indent_for_learn = "\n\t\t\t"
        file.write('<aiml version="1.0.1" encoding="UTF-8">'
                   '\n\t<category>'
                   '\n\t\t<pattern>LOAD AIML FILES</pattern>'
                   '\n\t\t<template>'
                   '\n\t\t\t<learn>chatBot/basic-chat-functions.aiml</learn>'
                    f'{reduce(lambda i, j: f"{i}{nl_indent_for_learn}<learn>chatBot/{replaceXMLSpecialChar(j)}.aiml</learn>", [""] + allTopics)}'
		           '\n\t\t</template>'
	               '\n\t</category>'
                   '\n</aiml>')


file_path = (base_path / "../data/cleaned-up-corpus.pickle").resolve()
filteredCorpus = pickle.load(open(file_path, "rb" ))

file_path = (base_path / "../data/result-topic.pickle").resolve()
resultTopics = pickle.load(open(file_path, "rb" ))

extractFacts = ExtractFacts()

print(resultTopics["topic_mapping"])

getAllTopics = [re.match("(\w+)(?:\/\w+)?", topic).group(1) for topic in resultTopics["topic_mapping"] if topic] #change when changing dic definition
createPilotFile(getAllTopics)

for topic_idx, topic in enumerate(resultTopics["topic_mapping"]):
    if topic:
        corpus_per_topic = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for cluster_idx, cluster in enumerate(resultTopics["clusters"]):
            if cluster == topic_idx:
                corpus_per_topic['url'].append(filteredCorpus['url'][cluster_idx])
                corpus_per_topic['scrapped_date'].append(filteredCorpus['scrapped_date'][cluster_idx])
                corpus_per_topic['published_date'].append(filteredCorpus['published_date'][cluster_idx])
                corpus_per_topic['data'].append(filteredCorpus["data"][cluster_idx])

        allStatements = extractFacts.extract(corpus_per_topic)


        newTopic =  re.match("(\w+)(?:\/\w+)?", topic).group(1) #Temporary solution, revisit data structure

        print(len(allStatements))
        createTopic([newTopic], allStatements)



#pd.DataFrame(corpus['data'], {url..., scrapped..}

#pandaframe
