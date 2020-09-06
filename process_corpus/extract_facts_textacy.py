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
    all_statements = set()
    for segment in corpus["data"]:
        segment_expanded = expand_contractions(segment)
        nlp_segment = nlp(segment_expanded)
        verb = None
        reflexive_pronouns = {"you": "I", "i", "you"}
        for token in doc:
            if token.dep_ == 'ROOT':
                verb = token.lemma_
        if verb:
            nouns = [token.text if token.text.lowercase() not in ["you, i"] else reflexive_pronouns[token.text.lowercase() ] for token in doc.noun_chunks]
            sentence = segment_expanded

    return all_statements


doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
doc = nlp('random shit no verb')

a = textacy.extract.entities(doc, exclude_types=["DATE", "MONEY", "ORDINAL"])
c = textacy.extract.subject_verb_object_triples(doc)

for b in a:
    print(b)

for b in c:
    print(b)

statements = textacy.extract.semistructured_statements(doc, "authorities")
for statement in statements:
    print(statement)


#Identifie, le verbe root, lemmatise -> c'est le cue

#Take le noun_chunk,

print([(token.text,token.dep_) for token in doc])
print([token.text for token in doc.noun_chunks])