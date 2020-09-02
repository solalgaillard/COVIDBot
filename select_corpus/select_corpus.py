import spacy
import pickle
from process_corpus.utilities import *
from process_corpus.segment_documents_textsplit import segment_documents_textsplit
from process_corpus.solve_coreferences_neuralcoref import solve_coreferences_neuralcoref
from process_corpus.features_extraction import FeatureExtraction
from export_to_aiml.aiml_export import export_to_aiml
from pathlib import Path

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

base_path = Path(__file__).parent

#Data ^ Come from the scrapper
file_path = (base_path / "../data_saved/scrapped-data-binary.pickle").resolve()
corpus = pickle.load(open(file_path, "rb" ))


corpus = remove_duplicates_in_corpus(corpus)

#corpus['data'] = remove_overused_sentences_from_corpus(corpus['data'])
corpus['data'] = [segment_documents_textsplit(solve_coreferences_neuralcoref(document)) for document in corpus['data']]

file_path = (base_path / "../data_saved/coreferences_solved_and_segmented_corpus.pickle").resolve()
with open(file_path, 'wb+') as f:
    pickle.dump(corpus, f)
print("Wrote to file coreferences_solved_and_segmented_corpus.pickle")

#Activated by option
####################
#
#export_scrapped_data_to_file_for_labeling(corpus)
####################





feature_extraction = FeatureExtraction()

#Activated by option
####################
#
#feature_extractions.trainModelLogRegr()


##Need to be able to save the model in a file
feature_extraction.trainModelSVC()



filteredCorpus = each_segement_gets_description(corpus)


#Filter out non-covid data
filteredCorpus = feature_extraction.useModel(filteredCorpus)



file_path = (base_path / "../data_saved/only_covid_corpus.pickle").resolve()
with open(file_path, 'wb+') as f:
    pickle.dump(filteredCorpus, f)
'''

file_path = (base_path / "../data_saved/cleaned-up-corpus.pickle").resolve()
filteredCorpus = pickle.load(open(file_path, "rb" ))
'''

'''

#TODO - Opearation ici, c'est df avec chaque segment
'''


result_topics = feature_extractions.featureExtraction(filteredCorpus["data"])


'''
file_path = (base_path / "../data_saved/cleaned-up-corpus.pickle").resolve()
filteredCorpus = pickle.load(open(file_path, "rb" ))

file_path = (base_path / "../data_saved/result-topic.pickle").resolve()
resultTopics = pickle.load(open(file_path, "rb" ))
'''
#extractFacts = ExtractFacts()

print(resultTopics["topic_mapping"])
export_to_aiml(result_topics)



#pd.DataFrame(corpus['data'], {url..., scrapped..}

#pandaframe
