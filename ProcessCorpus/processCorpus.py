import spacy
import nltk
import numpy as np

stopword_list = nltk.corpus.stopwords.words('english')
nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)

import neuralcoref
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

astring = "Ann-Marie Imrie’s first pregnancy ended in a stillbirth. She says the Safer Baby Bundle program treats the trauma of stillbirth as a problem that needs fixing."

def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


def return_POS(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner les étiquettes de chaque token
    return [(X, X.pos_) for X in doc]


def return_NER(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte et le label pour chaque entité
    return [(X.text, X.label_) for X in doc.ents]


def return_mean_embedding(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner la moyenne des vecteurs pour chaque phrase
    return np.mean([(X.vector) for X in doc], axis=0)

test_1 = nlp("I love pasta")
test_2 = nlp("Pasta is what I love")
test_3 = "I think it's right"


'''
lemmatize and stopwords then
'''
print(test_1.similarity(test_2))

'''
Take out all questions

'''

print(return_POS(astring))

print(return_NER(astring))

print(np.linalg.norm(return_mean_embedding(test_1)-return_mean_embedding(test_2)))
print(np.linalg.norm(return_mean_embedding(test_1)-return_mean_embedding(test_3)))

doc = nlp(astring)

print(doc._.has_coref)
print(doc._.coref_resolved)