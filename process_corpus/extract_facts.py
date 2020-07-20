import spacy
import textacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)


class ExtractFacts():
    def extract(self, corpus):
        #get verb lemma
        nounIndices = []
        for token in doc:
            # print(token.text, token.pos_, token.dep_, token.head.text)
            if token.pos_ == 'PROPN':
                nounIndices.append(index)

        for token in doc:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                  [child for child in token.children])

        #nsubj

        #ROOT

        #VERB
        #too
