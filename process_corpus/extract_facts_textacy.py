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
