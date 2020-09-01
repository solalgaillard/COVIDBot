import spacy
import textacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
"""
Les statements se décomposent en entité sujet, cue verbe, et fact fait.
"""
def extract_facts_textacy(corpus):
    allStatements = set()
    for segment in corpus["data"]:
        newSegment = nlp(segment)
        for chunk in newSegment.noun_chunks:
            if chunk.root.dep_ == "nsubj" and chunk.root.text.lower() not in ["who, which, what, where, how, when"]:
                statements = textacy.extract.semistructured_statements(newSegment, chunk.text)
                for statement in statements:
                    allStatements.add(statement)

    return allStatements
