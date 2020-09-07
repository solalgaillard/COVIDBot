from process_corpus.utilities import expand_contractions
import spacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
"""
    Les statements se décomposent en entité sujet, verbe, et fait.
    On garde le tout dans un dictionnaire. On utilise textacy pour
    extraire toutes les structures grammaticales qui s'articulent comme
    des faits.
"""

def extract_facts(corpus):
    all_statements = []
    for segment in corpus["data"]:
        segment_expanded = expand_contractions(segment)
        nlp_segment_expanded = nlp(segment_expanded)
        for sentence in nlp_segment_expanded.sents:
            dobjs = []
            nsubj = None
            verb = None
            for token in sentence:
                if token.dep_ == 'dobj':
                    dobjs.append(token.text)

                if not nsubj and token.dep_ == 'nsubj':
                    if token.text == "I":
                        nsubj = "you"
                    elif token.text.lower() == "you":
                        nsubj = "I"
                    else:
                        nsubj = token.text

                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    verb = token.lemma_
            if verb and nsubj and len(dobjs):
                if not any(stmt['nsubj'] == nsubj and stmt['verb'] == verb and stmt['dobjs'] == dobjs and stmt['sentence'] == sentence.text for stmt in all_statements):
                    all_statements.append({"nsubj": nsubj, "verb": verb, "dobjs": dobjs, "sentence": sentence.text})
    return all_statements


