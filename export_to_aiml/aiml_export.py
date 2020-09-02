from process_corpus.utilities import *
from process_corpus.extract_facts_textacy import extract_facts_textacy

def createPilotFile(all_existing_topics):
    with open(f'./chat_bot/covid_bot.aiml', "w+", encoding="utf-8") as file:
        nl_indent_for_learn = "\n\t\t\t"
        file.write('<aiml version="1.0.1" encoding="UTF-8">'
                   '\n\t<category>'
                   '\n\t\t<pattern>LOAD AIML FILES</pattern>'
                   '\n\t\t<template>'
                   '\n\t\t\t<learn>chat_bot/general/basic_chat_functions.aiml</learn>'
                    f'{reduce(lambda i, j: f"{i}{nl_indent_for_learn}<learn>chat_bot/covid_topics/{replaceXMLSpecialChar(j)}.aiml</learn>", [""] + all_existing_topics)}'
		           '\n\t\t\t<learn>chat_bot/general/covid_no_topic.aiml</learn>'
		           '\n\t\t</template>'
	               '\n\t</category>'
                   '\n</aiml>')


def setTopicString(topics):
    allTopicSetters = ""

    for topic in topics:
        allPatterns = [f'* {topic.upper()} *', f'{topic.upper()} *', f'* {topic.upper()}', topic.upper()]
        for pattern in allPatterns:
            allTopicSetters += ('\n\t<category>'
                               f'\n\t\t<pattern>{replaceXMLSpecialChar(pattern)}</pattern>'
                               '\n\t\t<template>'
                               f'\n\t\t\t<think><set name = "topic">{replaceXMLSpecialChar(topics[0].upper())}</set></think>'
                               f'\n\t\t\tI know a lot about {replaceXMLSpecialChar(topic)}'
                               '\n\t\t</template>'
                               '\n\t</category>')


    return allTopicSetters

# on regrette l'absence d'aiml 2... avec le caret comme wildcard
def setAllPermutationsString(all_statements):

    allPermutations = ""

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
            #currentFact = entity.text.capitalize() + ' ' + cue.text + ' ' + fact.text + '.'
            tmp = f'{entity.text.capitalize()} {cue.text} {fact.text}.'
            template += f'\n\t\t\t\t\t<li>{replaceXMLSpecialChar(tmp)}</li>'
        for pattern in allPatterns:
            allPermutations += ('\n\t\t<category>'
                                f'\n\t\t\t<pattern>{replaceXMLSpecialChar(pattern)}</pattern>'
                                f'\n\t\t\t<template>'
                                f'\n\t\t\t\t<random>'
                                f'{template}'
                                f'\n\t\t\t\t\t</random>'
                                f'\n\t\t\t</template>'
                                '\n\t\t</category>')



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
            template += f'\n\t\t\t\t\t<li>{replaceXMLSpecialChar(tmp)}</li>'
        for pattern in allPatterns:
            allPermutations += ('\n\t\t<category>'
                                f'\n\t\t\t<pattern>{replaceXMLSpecialChar(pattern)}</pattern>'
                                f'\n\t\t\t<template>'
                                f'\n\t\t\t\t<random>'
                                f'{template}'
                                f'\n\t\t\t\t\t</random>'
                                f'\n\t\t\t</template>'
                                '\n\t\t</category>')


    return allPermutations




def createTopic(allTopics, statements):
    with open(f'./chat_bot/covid_topics/{allTopics[0]}.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{setTopicString(allTopics)}'
                   f'\n\t<topic name = "{allTopics[0].upper()}">'
                   f'{setAllPermutationsString(statements)}'
                   '\n\t\t<category>'
                   '\n\t\t\t<pattern>*</pattern>'
                   '\n\t\t\t<template>'
                   '\n\t\t\t\t<think><set name="topic"><!-- No Topic --></set></think>'
                   '\n\t\t\t\tOk, changing topic.'
                   '\n\t\t\t</template>'
                   '\n\t\t</category>'
                   '\n\t</topic>'
                   '\n</aiml>')




def createNoTopic(statements):
    with open('./chat_bot/general/covid_no_topic.aiml', "w+", encoding="utf-8") as file:
        file.write('<aiml version = "1.0.1" encoding = "UTF-8">'
                   f'{setAllPermutationsString(statements)}'
                   '\n</aiml>')



def export_to_aiml(resultTopics):
    createPilotFile([topic[0] for topic in resultTopics["topic_mapping"]])

    corpus_without_topics = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    for topic_idx, topic in enumerate(resultTopics["topic_mapping"]):
        corpus_per_cluster = {'url': [], 'data': [], 'scrapped_date': [], 'published_date': []}
    for cluster_idx, cluster in enumerate(resultTopics["clusters"]):
        print(cluster, cluster_idx, topic_idx)
    if cluster == topic_idx:
        corpus_per_cluster['url'].append(filteredCorpus['url'][cluster_idx])
    corpus_per_cluster['scrapped_date'].append(filteredCorpus['scrapped_date'][cluster_idx])
    corpus_per_cluster['published_date'].append(filteredCorpus['published_date'][cluster_idx])
    corpus_per_cluster['data'].append(filteredCorpus["data"][cluster_idx])

    allStatements = extract_facts_textacy(corpus_per_cluster)
    if topic:
        createTopic(topic, allStatements)
    else:
        corpus_without_topics['url'].extend(corpus_per_cluster['url'])
    corpus_without_topics['scrapped_date'].extend(corpus_per_cluster['scrapped_date'])
    corpus_without_topics['published_date'].extend(corpus_per_cluster['published_date'])
    corpus_without_topics['data'].extend(corpus_per_cluster['data'])

    createNoTopic(extract_facts_textacy(corpus_without_topics))