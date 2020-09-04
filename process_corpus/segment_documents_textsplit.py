import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import spacy
from textsplit.algorithm import split_optimal
from textsplit.tools import get_penalty, get_segments

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

"""
    En utilisant textsplit, nous pouvons découper le texte en segment. textsplit utilise
    word2vec pour vectoriser les phrases puis calcule la similarité par mesure cosinus des 
    phrases entre elles et forme des segments ainsi.
"""
def segment_documents_textsplit(document):
    # Taille cible segment
    a_segment_len = len(document) / 1000. * 2
    # Spacy load
    nlp_document = nlp(document)

    # Découpage en phrases
    sentences_in_doc = [sent.text for sent in nlp_document.sents]

    # Liste d'entrées uniques du vocabulaire
    vocab_in_doc =  list(dict.fromkeys([token.text for token in nlp_document]))

    # Vectorisation de tous les mots
    vectors = [nlp(x).vector for x in vocab_in_doc]

    # Pandasframe avec vecteurs et mot
    wrdvecs = pd.DataFrame(vectors, index=vocab_in_doc)

    # Crée une vectorisation des phrases par produit scalaire de chaque mot de la phrase
    vecr = CountVectorizer(vocabulary=wrdvecs.index)
    sentence_vectors = vecr.transform(sentences_in_doc).dot(wrdvecs)

    # Si le vecteur a autant de mots que la taille cible d'un segment,
    # on renvoie le document comme ça
    if sentence_vectors.shape[0]/a_segment_len < 2:
        return [document]

    # Sinon, on définit le paramètre de pénalité.
    penalty = get_penalty([sentence_vectors], a_segment_len)

    # Puis on ségmente
    optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=20)
    segmented_text = get_segments(sentences_in_doc, optimal_segmentation)

    # Applatit la liste avec espaces entre phrases
    return [ ' '.join(x) for x in segmented_text]