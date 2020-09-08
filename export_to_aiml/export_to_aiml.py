from collections import Iterable
from functools import reduce
from math import sqrt
from process_corpus.extract_facts import extract_facts
from process_corpus.utilities import *

'''
    Création d'un fichier aiml pilot qui contient les références
    de tous les autres fichiers créés.
'''
def _create_pilot_file(all_existing_topics, nbr_of_no_topics):
    with open(f'./chat_bot_files/covid_bot.aiml', "w+", encoding="utf-8") as file:
        nl_indent_for_learn = "\n\t\t\t"
        file.write('<aiml version="1.0.1" encoding="UTF-8">'
                   '\n\t<category>'
                   '\n\t\t<pattern>LOAD AIML FILES</pattern>'
                   '\n\t\t<template>'
                   f'{reduce(lambda i, j: f"{i}{nl_indent_for_learn}<learn>chat_bot_files/covid_topics/{replace_xml_special_char(j)}.aiml</learn>", [""] + all_existing_topics)}'
		           f'{reduce(lambda i, j: f"{i}{nl_indent_for_learn}<learn>chat_bot_files/general/covid_no_topics_{j+1}.aiml</learn>", [""] + list(range(nbr_of_no_topics)))}'
		           '\n\t\t\t<learn>chat_bot_files/general/basic_chat_functions.aiml</learn>'
		           '\n\t\t</template>'
	               '\n\t</category>'
                   '\n</aiml>')

'''
    Crée toute les permutations pour la génération
    de la balise topic. On aurait aimé les wildcards d'AIML 2.0.
    Cela aurait évité tout ce "bloating".
'''
def _set_topic_string(topics):
    all_topic_setters = ""
    for topic in topics:
        # Précédence avec opérateur "_"
        all_patterns = [f'_ {topic.upper()} _', f'{topic.upper()} _', f'_ {topic.upper()}', topic.upper()]
        for pattern in all_patterns:
            all_topic_setters += ('\n\t<category>'
                               f'\n\t\t<pattern>{replace_xml_special_char(pattern)}</pattern>'
                               '\n\t\t<template>'
                               '\n\t\t\t<think>'
                               f'<set name = "topic">{replace_xml_special_char(topics[0].upper())}</set>'
                               '</think>'
                               f'\n\t\t\tYes, let us speak about {replace_xml_special_char(topic)}.'
                               '\n\t\t</template>'
                               '\n\t</category>')

    return all_topic_setters

'''
    Génére la catégorie avec pattern et réponses.
'''
def _create_permutation(pattern,template):
    return ('\n\t\t<category>'
            f'\n\t\t\t<pattern>{replace_xml_special_char(pattern)}</pattern>'
            '\n\t\t\t<template>'
            '\n\t\t\t\t<random>'
            f'{template}'
            '\n\t\t\t\t\t</random>'
            '\n\t\t\t</template>'
            '\n\t\t</category>')

'''
    Crée toute les permutations pour la génération
    de chaque pattern avec sujet, verbe, objet et
    toutes les possibilités d'agencements.
    Enfin, les sujets seuls sont aussi ajoutés en
    dernier ressort.
'''
def _set_all_permutations_string(all_statements, flag=[]):

    all_permutations = ""

    nsubj_verb_dobj_dic = {}

    nsubj_dic = {}

    for statement in all_statements:
        nsubj = statement['nsubj']
        verb = statement['verb']
        dobjs =  statement['dobjs']
        sentence = statement['sentence']

        # On ne pollue pas les patterns de thèmes afin de toujours pouvoir les
        # lancer.
        if nsubj.lower() not in flag and verb.lower() not in flag:
            for dobj in dobjs:
                if dobj.lower() not in flag:
                    # Pour chaque trio sujet, verbe, objet et pour tous les objets, on met dans un
                    # dictionnaire et on utilise chaque trio comme clé afin que toutes les phrases
                    # répondent la même pattern
                    if(f'{nsubj.upper()}{verb.upper()}{dobj.upper()}' in nsubj_verb_dobj_dic):
                        nsubj_verb_dobj_dic[f'{nsubj.upper()}{verb.upper()}{dobj.upper()}']['facts'].append(sentence)
                    else:
                        nsubj_verb_dobj_dic[f'{nsubj.upper()}{verb.upper()}{dobj.upper()}'] = {"facts": [sentence], "entity": nsubj, "cue": verb, "obj": dobj}
            # En dernier ressort, on fait une pattern simple juste sur le sujet
            if (nsubj.upper() in nsubj_dic):
                nsubj_dic[nsubj.upper()]['facts'].append(sentence)
            else:
                nsubj_dic[nsubj.upper()] = {"facts": [sentence], "entity": nsubj}

    # On inscrit toutes les patterns pour le trio sujet, verbe, objet.
    # Et on y ajoute les phrases.
    for statement in nsubj_verb_dobj_dic:
        entity = nsubj_verb_dobj_dic[statement]["entity"]
        cue = nsubj_verb_dobj_dic[statement]["cue"]
        obj = nsubj_verb_dobj_dic[statement]["obj"]
        facts = nsubj_verb_dobj_dic[statement]["facts"]
        template = ""
        all_patterns = [
            f'*{cue.upper()} * {entity.upper()} * {obj.upper()} *',
            f'* {cue.upper()} * {entity.upper()} * {obj.upper()}',
            f'* {cue.upper()} * {entity.upper()} {obj.upper()} *',
            f'* {cue.upper()}  {entity.upper()} * {obj.upper()} *',
            f'{cue.upper()} * {entity.upper()} * {obj.upper()} *',
            f'* {cue.upper()} * {entity.upper()} {obj.upper()}',
            f'* {cue.upper()} {entity.upper()} * {obj.upper()} *',
            f'{cue.upper()} * {entity.upper()} * {obj.upper()}',
            f'{cue.upper()} * {entity.upper()} {obj.upper()} *',
            f'{cue.upper()} {entity.upper()} {obj.upper()} *',
            f'{cue.upper()} {entity.upper()} * {obj.upper()}',
            f'{cue.upper()} * {entity.upper()} {obj.upper()}',
            f'* {cue.upper()} {entity.upper()} {obj.upper()}',
            f'* {entity.upper()} * {cue.upper()} * {obj.upper()} *',
            f'* {entity.upper()} * {cue.upper()} * {obj.upper()}',
            f'* {entity.upper()} * {cue.upper()} {obj.upper()} *',
            f'* {entity.upper()}  {cue.upper()} * {obj.upper()} *',
            f'{entity.upper()} * {cue.upper()} * {obj.upper()} *',
            f'* {entity.upper()} * {cue.upper()} {obj.upper()}',
            f'* {entity.upper()} {cue.upper()} * {obj.upper()} *',
            f'{entity.upper()} * {cue.upper()} * {obj.upper()}',
            f'{entity.upper()} * {cue.upper()} {obj.upper()} *',
            f'{entity.upper()} {cue.upper()} {obj.upper()} *',
            f'{entity.upper()} {cue.upper()} * {obj.upper()}',
            f'{entity.upper()} * {cue.upper()} {obj.upper()}',
            f'* {entity.upper()} {cue.upper()} {obj.upper()}',
            f'* {obj.upper()} * {cue.upper()} * {entity.upper()} *',
            f'* {obj.upper()} * {cue.upper()} * {entity.upper()}',
            f'* {obj.upper()} * {cue.upper()} {entity.upper()} *',
            f'* {obj.upper()}  {cue.upper()} * {entity.upper()} *',
            f'{obj.upper()} * {cue.upper()} * {entity.upper()} *',
            f'* {obj.upper()} * {cue.upper()} {entity.upper()}',
            f'* {obj.upper()} {cue.upper()} * {entity.upper()} *',
            f'{obj.upper()} * {cue.upper()} * {entity.upper()}',
            f'{obj.upper()} * {cue.upper()} {entity.upper()} *',
            f'{obj.upper()} {cue.upper()} {entity.upper()} *',
            f'{obj.upper()} {cue.upper()} * {entity.upper()}',
            f'{obj.upper()} * {cue.upper()} {entity.upper()}',
            f'* {obj.upper()} {cue.upper()} {entity.upper()}',
            f'* {cue.upper()} * {obj.upper()} * {entity.upper()} *',
            f'* {cue.upper()} * {obj.upper()} * {entity.upper()}',
            f'* {cue.upper()} * {obj.upper()} {entity.upper()} *',
            f'* {cue.upper()}  {obj.upper()} * {entity.upper()} *',
            f'{cue.upper()} * {obj.upper()} * {entity.upper()} *',
            f'* {cue.upper()} * {obj.upper()} {entity.upper()}',
            f'* {cue.upper()} {obj.upper()} * {entity.upper()} *',
            f'{cue.upper()} * {obj.upper()} * {entity.upper()}',
            f'{cue.upper()} * {obj.upper()} {entity.upper()} *',
            f'{cue.upper()} {obj.upper()} {entity.upper()} *',
            f'{cue.upper()} {obj.upper()} * {entity.upper()}',
            f'{cue.upper()} * {obj.upper()} {entity.upper()}',
            f'* {cue.upper()} {obj.upper()} {entity.upper()}',
            f'* {entity.upper()} * {obj.upper()} * {cue.upper()} *',
            f'* {entity.upper()} * {obj.upper()} * {cue.upper()}',
            f'* {entity.upper()} * {obj.upper()} {cue.upper()} *',
            f'* {entity.upper()}  {obj.upper()} * {cue.upper()} *',
            f'{entity.upper()} * {obj.upper()} * {cue.upper()} *',
            f'* {entity.upper()} * {obj.upper()} {cue.upper()}',
            f'* {entity.upper()} {obj.upper()} * {cue.upper()} *',
            f'{entity.upper()} * {obj.upper()} * {cue.upper()}',
            f'{entity.upper()} * {obj.upper()} {cue.upper()} *',
            f'{entity.upper()} {obj.upper()} {cue.upper()} *',
            f'{entity.upper()} {obj.upper()} * {cue.upper()}',
            f'{entity.upper()} * {obj.upper()} {cue.upper()}',
            f'* {entity.upper()} {obj.upper()} {cue.upper()}',
            f'* {obj.upper()} * {entity.upper()} * {cue.upper()} *',
            f'* {obj.upper()} * {entity.upper()} * {cue.upper()}',
            f'* {obj.upper()} * {entity.upper()} {cue.upper()} *',
            f'* {obj.upper()}  {entity.upper()} * {cue.upper()} *',
            f'{obj.upper()} * {entity.upper()} * {cue.upper()} *',
            f'* {obj.upper()} * {entity.upper()} {cue.upper()}',
            f'* {obj.upper()} {entity.upper()} * {cue.upper()} *',
            f'{obj.upper()} * {entity.upper()} * {cue.upper()}',
            f'{obj.upper()} * {entity.upper()} {cue.upper()} *',
            f'{obj.upper()} {entity.upper()} {cue.upper()} *',
            f'{obj.upper()} {entity.upper()} * {cue.upper()}',
            f'{obj.upper()} * {entity.upper()} {cue.upper()}',
            f'* {obj.upper()} {entity.upper()} {cue.upper()}',
        ]
        for fact in facts:
            template += f'\n\t\t\t\t\t<li>{replace_xml_special_char(capitalize_and_leave_string_untouched(fact))}</li>'
        for pattern in all_patterns:
            all_permutations += _create_permutation(pattern, template)

    # De même pour le solo sujet
    for statement in nsubj_dic:
        entity = nsubj_dic[statement]["entity"]
        facts = nsubj_dic[statement]["facts"]
        template = ""
        all_patterns = [
            f'* {entity.upper()} *',
            f'{entity.upper()} *',
            f'* {entity.upper()}',
            f'{entity.upper()}',
        ]
        for fact in facts:
            # currentFact = entity.text.capitalize() + ' ' + cue.text + ' ' + fact.text + '.'
            #tmp = f'{entity.text.capitalize()} {cue.text} {fact.text}.'
            template += f'\n\t\t\t\t\t<li>{replace_xml_special_char(capitalize_and_leave_string_untouched(fact))}</li>'
        for pattern in all_patterns:
            all_permutations += _create_permutation(pattern, template)


    return all_permutations



'''
    Structure pour chaque fichier sujet/thème.
'''
def _create_topic(all_topics, statements):
    with open(f'./chat_bot_files/covid_topics/{all_topics[0]}.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{_set_topic_string(all_topics)}'
                   f'\n\t<topic name = "{all_topics[0].upper()}">'
                   f'{_set_all_permutations_string(statements)}'
                   '\n\t\t<category>'
                   '\n\t\t\t<pattern>*</pattern>'
                   '\n\t\t\t<template>'
                   '\n\t\t\t\t<think><set name="topic"><!-- No Topic --></set></think>'
                   '\n\t\t\t\tOk, changing topic.'
                   '\n\t\t\t</template>'
                   '\n\t\t</category>'
                   '\n\t</topic>'
                   '\n</aiml>')

'''
    Petite fonction d'aide qui permet de découper des listes en sous-listes.
    Utilisé pour ne pas avoir des fichiers mastodontes.
'''
def _chunk_a_list(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]


'''
    Petite fonction d'aide qui applatit une liste de chaînes et retire les
    entités nulles.
'''
def _flatten_and_lowercase(list):
    for entry in list:
            if isinstance(entry, Iterable) and not isinstance(entry, str):
                for sub_entry in _flatten_and_lowercase(entry):
                    yield sub_entry.lower()
            elif entry:
                yield entry.lower()

'''
    Structure pour chaque fichier qui s'occupent des entrées hors-thèmes.
'''
def _create_no_topic(statements, it, flag):
    with open(f'./chat_bot_files/general/covid_no_topics_{it+1}.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{_set_all_permutations_string(statements, flag)}'
                   '\n</aiml>')

'''
    Fonction pilote. On récupère toutes les entrées par thème sur chaque cluster
    et on les injecte dans les fichiers thèmes. On garde aussi ces données et on les
    injecte dans les fichiers non-thèmes, histoire de pouvoir quand même avoir un
    corpus large, or "topic".
'''
def export_to_aiml(result_topics, corpus, memlim):
    all_statements = []
    corpus_without_topics = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}

    for topic_idx, topic in enumerate(result_topics["topic_mapping"]):
        corpus_per_cluster = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for cluster_idx, cluster in enumerate(result_topics["clusters"]):
            if cluster == topic_idx:
                corpus_per_cluster['url'].append(corpus['url'][cluster_idx])
                corpus_per_cluster['scrapped_date'].append(corpus['scrapped_date'][cluster_idx])
                corpus_per_cluster['published_date'].append(corpus['published_date'][cluster_idx])
                corpus_per_cluster['data'].append(corpus["data"][cluster_idx])

        statements_by_topic = extract_facts(corpus_per_cluster)
        all_statements.extend(statements_by_topic)
        if topic:
            _create_topic(topic, statements_by_topic)
        else:
            corpus_without_topics['url'].extend(corpus_per_cluster['url'])
            corpus_without_topics['scrapped_date'].extend(corpus_per_cluster['scrapped_date'])
            corpus_without_topics['published_date'].extend(corpus_per_cluster['published_date'])
            corpus_without_topics['data'].extend(corpus_per_cluster['data'])
    all_statements.extend(extract_facts(corpus_without_topics))
    # On réduit le cas échéant le nombre d'entrées pour ne pas saturer la mémoire
    all_statements = all_statements[:int(len(all_statements)*1/sqrt(memlim))]
    # On divise en plus petits fichiers, les fichiers non thèmes
    idx = 0
    for chunk in list(_chunk_a_list(all_statements, 500)):
        _create_no_topic(chunk, idx, list(_flatten_and_lowercase(result_topics["topic_mapping"])))
        idx += 1
    _create_pilot_file([topic[0] for topic in result_topics["topic_mapping"] if topic], idx)