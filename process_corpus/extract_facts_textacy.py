from process_corpus.utilities import expand_contractions
import spacy
import textacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
"""
    Les statements se décomposent en entité sujet, verbe, et fait.
    On garde le tout dans un dictionnaire. On utilise textacy pour
    extraire toutes les structures grammaticales qui s'articulent comme
    des faits.
"""
def extract_facts_textacy(corpus):
    all_statements = set()
    for segment in corpus["data"]:
        nlp_segment = nlp(segment)
        for chunk in nlp_segment.noun_chunks:
            # Tant que le sujet n'est pas un pronom interrogatif
            if chunk.root.dep_ == "nsubj" and chunk.root.text.lower() not in ["who, which, what, where, how, when"]:
                statements = textacy.extract.semistructured_statements(nlp_segment, chunk.text)
                for statement in statements:
                    all_statements.add(statement)

    return all_statements

def extract_facts_textacy(corpus):
    all_statements = []
    reflexive_pronouns = {"you": "I", "i": "you"}
    for segment in corpus["data"]:
        segment_expanded = expand_contractions(segment)
        nlp_segment_expanded = nlp(segment_expanded)
        for sentence in nlp_segment_expanded.sents:
            has_dobj = False
            has_nsubj = False
            verb = None
            for token in sentence:
                if not has_dobj and token.dep_ == 'dobj':
                    has_dobj = True

                if not has_nsubj and token.dep_ == 'nsubj':
                    has_nsubj = True

                if token.dep_ == 'ROOT':
                    verb = token.lemma_
            if verb and has_nsubj and has_dobj:
                lowercase_token = token.text.lower()
                nouns = [token.text if lowercase_token not in ["you, i"] else reflexive_pronouns[lowercase_token] for token in sentence.noun_chunks]
                if not any(stmt['nouns'] == nouns and stmt['verb'] == verb and stmt['sentence'] == sentence.text for stmt in all_statements):
                    all_statements.append({"nouns": nouns, "verb": verb, "sentence": sentence.text})
    return all_statements


