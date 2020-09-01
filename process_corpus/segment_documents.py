from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd
nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

def segment_documents(document):
    a_segment_len = len(document) / 1000. * 2
    nlp_document = nlp(document)

    sentences_in_doc = [sent.text for sent in nlp_document.sents]
    vocab_in_doc =  list(dict.fromkeys([token.text for token in nlp_document]))
    vectors = [nlp(x).vector for x in vocab_in_doc]

    wrdvecs = pd.DataFrame(vectors, index=vocab_in_doc)
    vecr = CountVectorizer(vocabulary=wrdvecs.index)
    sentence_vectors = vecr.transform(sentences_in_doc).dot(wrdvecs)

    if sentence_vectors.shape[0]/a_segment_len < 2:
        return [document]

    penalty = get_penalty([sentence_vectors], a_segment_len)

    optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=20)
    segmented_text = get_segments(sentences_in_doc, optimal_segmentation)

    return [ ' '.join(x) for x in segmented_text]
