import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from contractions import CONTRACTION_MAP
from pathlib import Path
import unicodedata
from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal, split_greedy, get_total
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd
nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')

class SegmentDocuments():

    def segmentDocs(self, document):
        print(len(document))
        segment_len = len(document) / 1000. * 2

        sentenced_text = nltk.sent_tokenize(document)
        vocab = list(dict.fromkeys(nltk.word_tokenize(document)))

        vectors = [nlp(x).vector for x in vocab]

        wrdvecs = pd.DataFrame(vectors, index=vocab)
        vecr = CountVectorizer(vocabulary=wrdvecs.index)
        sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)
        print(segment_len, sentence_vectors.shape[0] )
        print(sentence_vectors.shape[0]/segment_len )
        #print(sentence_vectors)

        if sentence_vectors.shape[0]/segment_len < 2:
            return [document]

        penalty = get_penalty([sentence_vectors], segment_len)
        print('penalty %4.2f' % penalty)

        optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=20)
        segmented_text = get_segments(sentenced_text, optimal_segmentation)

        print('%d sentences, %d segments, avg %4.2f sentences per segment' % (
            len(sentenced_text), len(segmented_text), len(sentenced_text) / len(segmented_text)))

        newSegmentText = []
        for x in segmented_text:
            newSegmentText.append(' '.join(x))

        return newSegmentText

