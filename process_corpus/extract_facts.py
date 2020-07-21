import spacy
import textacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)


class ExtractFacts():
    def extract(self, corpus):
        #get verb lemma

        allStatements = set()
        nounIndices = []
        verbIndices = []
        for segment in corpus["data"]:
            segment = nlp(segment)
            for token in segment:
                # print(token.text, token.pos_, token.dep_, token.head.text)
                if token.dep_ == 'nsubj':
                    nounIndices.append(token.text)
                if token.dep_ == 'ROOT':
                    verbIndices.append(token.text)

        for noun in list(dict.fromkeys(nounIndices)):
            print(noun)
            for verb in list(dict.fromkeys(verbIndices)):
                print(verb)
                statements = textacy.extract.semistructured_statements(segment, noun, cue=verb)
                for statement in statements:
                    allStatements.add(statement)

        for statement in allStatements:
            entity, cue, fact = statement
            print("* entity:", entity, ", cue:", cue, ", fact:", fact)