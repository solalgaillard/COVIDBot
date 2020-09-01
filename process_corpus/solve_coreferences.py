from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal, split_greedy, get_total
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd
import neuralcoref


nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)

coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')


class solveCoreference():

    def belongsToWhichSentence(self, doc, idx):
        sentTokDel = [sent.start for sent in doc.sents]
        for index, item in enumerate(sentTokDel):
            if idx<item:
                return index-1



    def replaceOnlySentencesApart(self, document):
        newDoc = document
        document = nlp(document)

        clust = []
        for cluster in document._.coref_clusters:
            mainIdx = cluster.main.start
            for mention in cluster.mentions:
                clust.append({ "main": cluster.main, "mention": mention, "start": mention.start, "end": mention.end-1})


        newlist = sorted(clust, key=lambda k: k['start'])

        newnewlist = []
        for idx in range(len(newlist)):
            if( idx+1 < len(newlist) and newlist[idx]["end"] < newlist[idx+1]["start"]):
                newnewlist.append(newlist[idx])

        offset=0
        for mention in newlist:
            mainIdx = mention["main"].start
            sentenceIdx = self.belongsToWhichSentence(document, mainIdx)
            mentionStart = mention["start"]
            mentionEnd = mention["end"]
            sentenceMention = self.belongsToWhichSentence(document, mentionStart)
            if (mention["main"] != mention["mention"] and mainIdx != mentionStart and sentenceMention != sentenceIdx):
                docIdxStart = document[mentionStart].idx
                docIdxEnd = document[mentionEnd].idx + len(document[mentionEnd])
                newDoc = newDoc[: docIdxStart+offset] + mention["main"].text + newDoc[ docIdxEnd + offset : ]
                offset = offset + (len(mention["main"].text) - (docIdxEnd - docIdxStart))

        return newDoc


