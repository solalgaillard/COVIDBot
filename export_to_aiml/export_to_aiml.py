from functools import reduce
from process_corpus.extract_facts_textacy import extract_facts_textacy
from process_corpus.utilities import *

def _create_pilot_file(all_existing_topics):
    with open(f'./chat_bot_files/covid_bot.aiml', "w+", encoding="utf-8") as file:
        nl_indent_for_learn = "\n\t\t\t"
        file.write('<aiml version="1.0.1" encoding="UTF-8">'
                   '\n\t<category>'
                   '\n\t\t<pattern>LOAD AIML FILES</pattern>'
                   '\n\t\t<template>'
                   '\n\t\t\t<learn>chat_bot_files/general/basic_chat_functions.aiml</learn>'
                   f'{reduce(lambda i, j: f"{i}{nl_indent_for_learn}<learn>chat_bot_files/covid_topics/{replace_xml_special_char(j)}.aiml</learn>", [""] + all_existing_topics)}'
		           '\n\t\t\t<learn>chat_bot/general/covid_no_topic.aiml</learn>'
		           '\n\t\t</template>'
	               '\n\t</category>'
                   '\n</aiml>')


def _set_topic_string(topics):
    all_topic_setters = ""
    for topic in topics:
        all_patterns = [f'* {topic.upper()} *', f'{topic.upper()} *', f'* {topic.upper()}', topic.upper()]
        for pattern in all_patterns:
            all_topic_setters += ('\n\t<category>'
                               f'\n\t\t<pattern>{replace_xml_special_char(pattern)}</pattern>'
                               '\n\t\t<template>'
                               '\n\t\t\t<think>'
                               f'<set name = "topic">{replace_xml_special_char(topics[0].upper())}</set>'
                               '</think>'
                               f'\n\t\t\tI know a lot about {replace_xml_special_char(topic)}'
                               '\n\t\t</template>'
                               '\n\t</category>')

    return all_topic_setters


def _create_permutation(pattern,template):
    return ('\n\t\t<category>'
            f'\n\t\t\t<pattern>{replace_xml_special_char(pattern)}</pattern>'
            '\n\t\t\t<template>'
            '\n\t\t\t\t<random>'
            f'{template}'
            '\n\t\t\t\t\t</random>'
            '\n\t\t\t</template>'
            '\n\t\t</category>')

# on regrette l'absence d'aiml 2... avec le caret comme wildcard
def _set_all_permutations_string(all_statements):

    all_permutations = ""

    entity_cue_dic = {}

    entity_dic = {}

    for statement in all_statements:
        entity, cue, fact = statement

        if(f'{entity.text.upper()}{cue.text.upper()}' in entity_cue_dic):
            entity_cue_dic[f'{entity}{cue}']['facts'].append(fact)
        else:
            entity_cue_dic[f'{entity}{cue}'] = {"facts": [fact], "entity": entity, "cue": cue}

        if (entity.text.upper() in entity_dic):
            entity_dic[entity.text.upper()]['facts'].append(fact)
        else:
            entity_dic[entity.text.upper()] = {"facts": [fact], "entity": entity, "cue": cue}


    for statement in entity_cue_dic:
        entity = entity_cue_dic[statement]["entity"]
        cue = entity_cue_dic[statement]["cue"]
        facts = entity_cue_dic[statement]["facts"]
        template = ""
        allPatterns = [
            f'* {cue.text.upper()} * {entity.text.upper()} *',
            f'{cue.text.upper()} * {entity.text.upper()} *',
            f'{cue.text.upper()} {entity.text.upper()} *',
            f'* {cue.text.upper()} {entity.text.upper()}',
            f'* {cue.text.upper()} * {entity.text.upper()}',
            f'* {cue.text.upper()} {entity.text.upper()} *',
            f'{cue.text.upper()} * {entity.text.upper()}',
            f'{cue.text.upper()} {entity.text.upper()}',
        ]
        for fact in facts:
            tmp = f'{entity.text.capitalize()} {cue.text} {fact.text}.'
            template += f'\n\t\t\t\t\t<li>{replace_xml_special_char(tmp)}</li>'
        for pattern in allPatterns:
            all_permutations += _create_permutation(pattern, template)

    for statement in entity_dic:
        entity = entity_dic[statement]["entity"]
        cue = entity_dic[statement]["cue"]
        facts = entity_dic[statement]["facts"]
        template = ""
        allPatterns = [
            f'* {entity.text.upper()} *',
            f'{entity.text.upper()} *',
            f'* {entity.text.upper()}',
            f'{entity.text.upper()}',
        ]
        for fact in facts:
            # currentFact = entity.text.capitalize() + ' ' + cue.text + ' ' + fact.text + '.'
            tmp = f'{entity.text.capitalize()} {cue.text} {fact.text}.'
            template += f'\n\t\t\t\t\t<li>{replace_xml_special_char(tmp)}</li>'
        for pattern in allPatterns:
            all_permutations += _create_permutation(pattern, template)


    return all_permutations




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




def _create_no_topic(statements):
    with open('./chat_bot_files/general/covid_no_topic.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{_set_all_permutations_string(statements)}'
                   '\n</aiml>')



def export_to_aiml(result_topics, corpus):

    _create_pilot_file([topic[0] for topic in result_topics["topic_mapping"] if topic])

    corpus_without_topics = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    for topic_idx, topic in enumerate(result_topics["topic_mapping"]):
        corpus_per_cluster = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
        for cluster_idx, cluster in enumerate(result_topics["clusters"]):
            print(cluster, cluster_idx, topic_idx)
            if cluster == topic_idx:
                corpus_per_cluster['url'].append(corpus['url'][cluster_idx])
                corpus_per_cluster['scrapped_date'].append(corpus['scrapped_date'][cluster_idx])
                corpus_per_cluster['published_date'].append(corpus['published_date'][cluster_idx])
                corpus_per_cluster['data'].append(corpus["data"][cluster_idx])

        all_statements = extract_facts_textacy(corpus_per_cluster)
        if topic:
            _create_topic(topic, all_statements)
        else:
            corpus_without_topics['url'].extend(corpus_per_cluster['url'])
            corpus_without_topics['scrapped_date'].extend(corpus_per_cluster['scrapped_date'])
            corpus_without_topics['published_date'].extend(corpus_per_cluster['published_date'])
            corpus_without_topics['data'].extend(corpus_per_cluster['data'])

    _create_no_topic(extract_facts_textacy(corpus_without_topics))