import neuralcoref
import spacy

nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

"""
    En utilisant neuralcoref, un réseau neuronal à propagation avant qui utilise
    le parsing de Spacy pour résoudre les coreférences, je remplace dans le document
    les pronoms pour en faire des phrases qui ne réfèrent à aucun antécédent.
"""

'''

'''
def _belongs_to_which_sentence(nlp_document, idx):
    sent_tok_del = [sent.start for sent in nlp_document.sents]
    for index, item in enumerate(sent_tok_del):
        if idx<item:
            return index-1


'''
    Identifie les coréférences, regarde leurs indexs, prend la première référence et replace les autres par
    celle-ci. Fais tout ce processus en place
'''
def solve_coreferences_neuralcoref(document):
    new_document = document
    nlp_document = nlp(document)

    # Pour chaque cluster, on garde en mémoire où les références commencent et finissent
    all_clusters = []
    for cluster in nlp_document._.coref_clusters:
        for mention in cluster.mentions:
            all_clusters.append({ "main": cluster.main, "mention": mention, "start": mention.start, "end": mention.end-1})

    # On organise par ordre ascendant dans le texte, puisqu'on manipule en place.
    all_clusters = sorted(all_clusters, key=lambda k: k['start'])
    offset = 0

    # Remplace en place avec un offset qu'on garde en mémoire
    for mention in all_clusters:
        main_idx = mention["main"].start
        sentence_idx = _belongs_to_which_sentence(nlp_document, main_idx)
        mention_start = mention["start"]
        mention_end = mention["end"]
        sentence_mention = _belongs_to_which_sentence(nlp_document, mention_start)
        if (mention["main"] != mention["mention"] and main_idx != mention_start and sentence_mention != sentence_idx):
            doc_idx_start = nlp_document[mention_start].idx
            doc_idx_end = nlp_document[mention_end].idx + len(nlp_document[mention_end])
            new_document = new_document[: doc_idx_start+offset] + mention["main"].text + new_document[ doc_idx_end + offset : ]
            offset = offset + (len(mention["main"].text) - (doc_idx_end - doc_idx_start))

    return new_document


