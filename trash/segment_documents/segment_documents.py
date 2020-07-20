from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal, split_greedy, get_total
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd
import neuralcoref


nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)

coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')







#TODO - 1 - Coreference extraction. - done
#TODO - 2 - Text Segmentation - done
#TODO - 3 - Automatize to get a small corpus to label.


doc = nlp("Fauci Back at the White House, a Day After Trump Aides Tried to Undermine Him Fauci Back at the White House, a Day After Trump Aides Tried to Undermine Him The visit underscored a reality for both the president and his most prominent coronavirus adviser: They are stuck with each other. Dr. Anthony S. Fauci, the government’s top infectious disease expert, has served under presidents from both parties. WASHINGTON — A day after President Trump’s press office tried to undermine the reputation of the nation’s top infectious disease expert with an of what it said were his misjudgments in the early days of the coronavirus, Dr. Anthony S. Fauci returned to the White House on Monday. The visit underscored a reality for both men: They are stuck with each other. Dr. Fauci — who has not had direct contact with the president in more than five weeks even as the number of Americans with Covid-19, the disease caused by the coronavirus, has risen sharply in the Southwest — slipped back into the West Wing to meet with Mark Meadows, the White House chief of staff, while his allies denounced what they called a meanspirited and misguided effort by the White House to smear him. White House officials declined to comment on what was discussed in the conversation between Mr. Meadows, who has long expressed skepticism about the conclusions of the nation’s public health experts, and Dr. Fauci, though one official called it a good conversation and said they continued to have a positive relationship. For his part, Mr. Trump made no effort to sugarcoat his rift with Dr. Fauci, declining to repudiate the criticism of him from his staff and saying that “I don’t always agree with him. ” But the president also implicitly acknowledged how unlikely he was to get rid of Dr. Fauci, calling him “a very nice person” and saying that “I like him personally. ” Mr. Trump could formally remove Dr. Fauci from the official coronavirus task force, but that would be a relatively meaningless step because it no longer serves as the nerve-center of a pandemic response that the Trump administration has pushed governors to take responsibility for. As the director of the National Institute of Allergy and Infectious Diseases at the National Institutes of Health, Dr. Fauci is a career civil servant. Firing him would require a finding of cause of malfeasance, and would most likely end up tied up in lengthy appeals, though the president could still seek to sideline Dr. Fauci in meaningless work, transfer him to another location or cut his budget in an attempt to get him to resign. The anonymous accusations against Dr. Fauci were “enormously sad and totally inappropriate,” said Dr. Margaret Hamburg, a former special assistant to Dr. Fauci who served as commissioner of the Food and Drug Administration under President Barack Obama. “Never have we needed his expertise and focus more than right now. Why would we both undermine him and his ability to do his important work? ” Dr. Fauci is also a public figure unlike any other health official in the federal government, well known for his decades organizing its responses to diseases like AIDS and Ebola. In his office in Building 31 on the campus of the N. I.H. , he keeps a wall of photographs of himself with celebrities and presidents. Over time, he has learned to navigate the collisions between politics and health. That has never been more difficult than in this administration, but Dr. Fauci has recognized that to remain effective, he must navigate Mr. Trump’s mercurial moods and contempt for expertise. The two once enjoyed an occasionally bantering relationship, and the president several times followed Dr. Fauci’s advice to extend national stay-at-home guidance. But that was as far as it went; Mr. Trump calls Dr. Fauci “Anthony,” a name that few use for someone who prefers the more casual moniker “Tony. ” A record 5. 4 million people lost their health coverage amid the pandemic, a study found. Amid surging cases, California imposes a sweeping rollback of its reopening plans. Dr. Fauci’s international reputation has not spared him from the White House attacks, which and later in other news outlets. The criticism, which was distributed anonymously to reporters, detailed what the White House believed was a series of premature or contradictory recommendations that Dr. Fauci has made over the past several months as the virus bore down on the United States. For example, White House officials pointed to a statement by Dr. Fauci in a Feb. 29 interview that “at this moment, there is no need to change anything that you’re doing on a day-by-day basis. ” But they omitted a warning he delivered right after. , conducted by NBC News. “When you start to see community spread, this could change and force you to become much more attentive to doing things that would protect you from spread. ” In the same interview, Dr. Fauci also warned that the coronavirus could become “a major outbreak. ” Kayleigh McEnany, the White House press secretary, took ownership on Monday of the opposition research-style effort, saying that her office merely “provided a direct answer to what was a direct question” from The Post about whether Dr. Fauci had made mistakes during the course of the response. Even some of Dr. Fauci’s senior colleagues at the Department of Health and Human Services have begun to echo the White House. Adm. Brett P. Giroir, the assistant secretary for health and a fellow member of the coronavirus task force, said Sunday on NBC’s “Meet the Press” that Dr. Fauci “is not 100 percent right, and he also doesn’t necessarily — and he admits that — have the whole national interest in mind. ” Admiral Giroir added that Dr. Fauci “looks at it from a very narrow public health point of view. ” Dr. Fauci spent the early days of the pandemic as the leading scientific voice in the federal government’s response before falling out of favor with Mr. Trump and his top aides over blunt comments inconsistent with the president’s message of economic resurgence. In task force meetings, Dr. Fauci has often styled himself as a solitary pessimist in a room where some officials have been eager to wave away the alarming trajectory of the coronavirus. His analysis has sometimes clashed with another prominent public health figure on the task force, Dr. Deborah L. Birx, who has harnessed a flurry of projections and models to package a more hopeful picture of the outbreak. In the early days of the outbreak, Dr. Fauci, who typically sleeps only about five hours a night, lived mostly anonymously, taking the Washington Metro to the White House and Capitol Hill to brief lawmakers. He still spends late nights in his home office fielding calls from his boss, Dr. Francis Collins, the N. I.H. director, and from politicians like Andrew M. Cuomo, the governor of New York and a close friend. Dr. Fauci, 79, has for decades had broad access to the White House, where he once explained the AIDS epidemic to President Ronald Reagan. “There’s nothing unique or special about being the director of the National Institute of Allergy and Infectious Diseases that sets you up to be an adviser to presidents,” Dr. Hamburg said. “He has become that because of what he brings to the role. ” Standing next to Mr. Trump through a long string of task force briefings in March and April, he issued warnings about the ferocity of the virus’s spread and pleas to take it seriously. But his message began to wear on some Americans who viewed him as an avatar of government fear-mongering and overreach. At one point, a right-wing movement on Twitter using the hashtag #FireFauci picked up steam, and Mr. Trump one night retweeted a supporter who used the slogan, forcing the president to By early April, Dr. Fauci had received so many personal threats that he was assigned personal protection. The N. I.H. continues to turn over threats to the agency’s security force, said one official familiar with them. As Dr. Fauci’s prominence has risen, he has received a glut of media and event requests, forcing officials at the N. I.H. to monitor his email inbox. He became a ubiquitous presence on cable news. But as Dr. Fauci’s public assessments of the outbreak became increasingly dire, Mr. Meadows and several press officials he brought to the White House began to tighten the access television reporters had to him, ignoring or blocking requests routed to them from the N. I.H. Broadcast news requests for Dr. Fauci now go through Michael R. Caputo, the top spokesman at the Department of Health and Human Services, a loyal ally of the president’s who is still friendly with and supportive of Dr. Fauci. In a text on Monday, Mr. Caputo said that only some of the requests for Dr. Fauci had to be cleared by the White House. The White House’s attempts to discredit Dr. Fauci raised alarm on Monday among health experts who have long known him as public health’s most important ambassador. Dr. David Relman, a microbiologist at Stanford University, said that the White House’s campaign against its own top health expert was “dark, dark stain. ” “When you disrespect Tony on matters of public health science, you’re slapping in the face all of U. S. science,” said Dr. Relman, who has worked with Dr. Fauci for over 20 years. “Tony is in some ways the face of U. S. public health-oriented science. ” Barry Bloom, a professor of public health at Harvard, said that Dr. Fauci had become the default spokesman for scientific consensus in absence of the Centers for Disease Control and Prevention, which has maintained a quiet public role throughout the pandemic. “What Tony represents is the best that he can find about a scientific event and consensus,” said Dr. Bloom, who has known Dr. Fauci for over 40 years. “Tony doesn’t pop off on what’s in his head the moment it’s in his head. ” Dr. Relman said Dr. Fauci’s role in the federal government’s response to the AIDS epidemic prepared him for the dilemma of responding to complex outbreaks with “imperfect information. ” “He learned that science can be politicized,” Dr. Relman added, “even when your conversation partner isn’t someone who worships and respects science. ” Fauci Back at the White House, a Day After Trump Aides Tried to Undermine Him The visit underscored a reality for both the president and his most prominent coronavirus adviser: They are stuck with each other. Dr. Anthony S. Fauci, the government’s top infectious disease expert, has served under presidents from both parties. WASHINGTON — A day after President Trump’s press office tried to undermine the reputation of the nation’s top infectious disease expert with an of what it said were his misjudgments in the early days of the coronavirus, Dr. Anthony S. Fauci returned to the White House on Monday. The visit underscored a reality for both men: They are stuck with each other. Dr. Fauci — who has not had direct contact with the president in more than five weeks even as the number of Americans with Covid-19, the disease caused by the coronavirus, has risen sharply in the Southwest — slipped back into the West Wing to meet with Mark Meadows, the White House chief of staff, while his allies denounced what they called a meanspirited and misguided effort by the White House to smear him. White House officials declined to comment on what was discussed in the conversation between Mr. Meadows, who has long expressed skepticism about the conclusions of the nation’s public health experts, and Dr. Fauci, though one official called it a good conversation and said they continued to have a positive relationship. For his part, Mr. Trump made no effort to sugarcoat his rift with Dr. Fauci, declining to repudiate the criticism of him from his staff and saying that “I don’t always agree with him. ” But the president also implicitly acknowledged how unlikely he was to get rid of Dr. Fauci, calling him “a very nice person” and saying that “I like him personally. ” Mr. Trump could formally remove Dr. Fauci from the official coronavirus task force, but that would be a relatively meaningless step because it no longer serves as the nerve-center of a pandemic response that the Trump administration has pushed governors to take responsibility for. As the director of the National Institute of Allergy and Infectious Diseases at the National Institutes of Health, Dr. Fauci is a career civil servant. Firing him would require a finding of cause of malfeasance, and would most likely end up tied up in lengthy appeals, though the president could still seek to sideline Dr. Fauci in meaningless work, transfer him to another location or cut his budget in an attempt to get him to resign. The anonymous accusations against Dr. Fauci were “enormously sad and totally inappropriate,” said Dr. Margaret Hamburg, a former special assistant to Dr. Fauci who served as commissioner of the Food and Drug Administration under President Barack Obama. “Never have we needed his expertise and focus more than right now. Why would we both undermine him and his ability to do his important work? ” Dr. Fauci is also a public figure unlike any other health official in the federal government, well known for his decades organizing its responses to diseases like AIDS and Ebola. In his office in Building 31 on the campus of the N. I.H. , he keeps a wall of photographs of himself with celebrities and presidents. Over time, he has learned to navigate the collisions between politics and health. That has never been more difficult than in this administration, but Dr. Fauci has recognized that to remain effective, he must navigate Mr. Trump’s mercurial moods and contempt for expertise. The two once enjoyed an occasionally bantering relationship, and the president several times followed Dr. Fauci’s advice to extend national stay-at-home guidance. But that was as far as it went; Mr. Trump calls Dr. Fauci “Anthony,” a name that few use for someone who prefers the more casual moniker “Tony. ” A record 5. 4 million people lost their health coverage amid the pandemic, a study found. Amid surging cases, California imposes a sweeping rollback of its reopening plans. Dr. Fauci’s international reputation has not spared him from the White House attacks, which and later in other news outlets. The criticism, which was distributed anonymously to reporters, detailed what the White House believed was a series of premature or contradictory recommendations that Dr. Fauci has made over the past several months as the virus bore down on the United States. For example, White House officials pointed to a statement by Dr. Fauci in a Feb. 29 interview that “at this moment, there is no need to change anything that you’re doing on a day-by-day basis. ” But they omitted a warning he delivered right after. , conducted by NBC News. “When you start to see community spread, this could change and force you to become much more attentive to doing things that would protect you from spread. ” In the same interview, Dr. Fauci also warned that the coronavirus could become “a major outbreak. ” Kayleigh McEnany, the White House press secretary, took ownership on Monday of the opposition research-style effort, saying that her office merely “provided a direct answer to what was a direct question” from The Post about whether Dr. Fauci had made mistakes during the course of the response. Even some of Dr. Fauci’s senior colleagues at the Department of Health and Human Services have begun to echo the White House. Adm. Brett P. Giroir, the assistant secretary for health and a fellow member of the coronavirus task force, said Sunday on NBC’s “Meet the Press” that Dr. Fauci “is not 100 percent right, and he also doesn’t necessarily — and he admits that — have the whole national interest in mind. ” Admiral Giroir added that Dr. Fauci “looks at it from a very narrow public health point of view. ” Dr. Fauci spent the early days of the pandemic as the leading scientific voice in the federal government’s response before falling out of favor with Mr. Trump and his top aides over blunt comments inconsistent with the president’s message of economic resurgence. In task force meetings, Dr. Fauci has often styled himself as a solitary pessimist in a room where some officials have been eager to wave away the alarming trajectory of the coronavirus. His analysis has sometimes clashed with another prominent public health figure on the task force, Dr. Deborah L. Birx, who has harnessed a flurry of projections and models to package a more hopeful picture of the outbreak. In the early days of the outbreak, Dr. Fauci, who typically sleeps only about five hours a night, lived mostly anonymously, taking the Washington Metro to the White House and Capitol Hill to brief lawmakers. He still spends late nights in his home office fielding calls from his boss, Dr. Francis Collins, the N. I.H. director, and from politicians like Andrew M. Cuomo, the governor of New York and a close friend. Dr. Fauci, 79, has for decades had broad access to the White House, where he once explained the AIDS epidemic to President Ronald Reagan. “There’s nothing unique or special about being the director of the National Institute of Allergy and Infectious Diseases that sets you up to be an adviser to presidents,” Dr. Hamburg said. “He has become that because of what he brings to the role. ” Standing next to Mr. Trump through a long string of task force briefings in March and April, he issued warnings about the ferocity of the virus’s spread and pleas to take it seriously. But his message began to wear on some Americans who viewed him as an avatar of government fear-mongering and overreach. At one point, a right-wing movement on Twitter using the hashtag #FireFauci picked up steam, and Mr. Trump one night retweeted a supporter who used the slogan, forcing the president to By early April, Dr. Fauci had received so many personal threats that he was assigned personal protection. The N. I.H. continues to turn over threats to the agency’s security force, said one official familiar with them. As Dr. Fauci’s prominence has risen, he has received a glut of media and event requests, forcing officials at the N. I.H. to monitor his email inbox. He became a ubiquitous presence on cable news. But as Dr. Fauci’s public assessments of the outbreak became increasingly dire, Mr. Meadows and several press officials he brought to the White House began to tighten the access television reporters had to him, ignoring or blocking requests routed to them from the N. I.H. Broadcast news requests for Dr. Fauci now go through Michael R. Caputo, the top spokesman at the Department of Health and Human Services, a loyal ally of the president’s who is still friendly with and supportive of Dr. Fauci. In a text on Monday, Mr. Caputo said that only some of the requests for Dr. Fauci had to be cleared by the White House. The White House’s attempts to discredit Dr. Fauci raised alarm on Monday among health experts who have long known him as public health’s most important ambassador. Dr. David Relman, a microbiologist at Stanford University, said that the White House’s campaign against its own top health expert was “dark, dark stain. ” “When you disrespect Tony on matters of public health science, you’re slapping in the face all of U. S. science,” said Dr. Relman, who has worked with Dr. Fauci for over 20 years. “Tony is in some ways the face of U. S. public health-oriented science. ” Barry Bloom, a professor of public health at Harvard, said that Dr. Fauci had become the default spokesman for scientific consensus in absence of the Centers for Disease Control and Prevention, which has maintained a quiet public role throughout the pandemic. “What Tony represents is the best that he can find about a scientific event and consensus,” said Dr. Bloom, who has known Dr. Fauci for over 40 years. “Tony doesn’t pop off on what’s in his head the moment it’s in his head. ” Dr. Relman said Dr. Fauci’s role in the federal government’s response to the AIDS epidemic prepared him for the dilemma of responding to complex outbreaks with “imperfect information. ” “He learned that science can be politicized,” Dr. Relman added, “even when your conversation partner isn’t someone who worships and respects science.")


def belongsToWhichSentence(doc, idx):
    sentTokDel = [sent.start for sent in doc.sents]
    for index, item in enumerate(sentTokDel):
        if idx<item:
            return index-1

newDoc = doc.text


#Invert burden on sent
#Take coref_clusters
#take start,
#For all clusters, struct -> mentionStart, mentionEnd ->¥ main

clust = []
for cluster in doc._.coref_clusters:
    mainIdx = cluster.main.start
    for mention in cluster.mentions:
        print(mention)
        clust.append({ "main": cluster.main, "mention": mention, "start": mention.start, "end": mention.end-1})

print(clust)

newlist = sorted(clust, key=lambda k: k['start'])

newnewlist = []
for idx in range(len(newlist)):
    print(newlist[idx])
    if( idx+1 < len(newlist) and newlist[idx]["end"] < newlist[idx+1]["start"]):
        newnewlist.append(newlist[idx])

print(newnewlist)




offset=0
for mention in newlist:
    print(mention)
    mainIdx = mention["main"].start
    sentenceIdx = belongsToWhichSentence(doc, mainIdx)
    mentionStart = mention["start"]
    mentionEnd = mention["end"]
    sentenceMention = belongsToWhichSentence(doc, mentionStart)
    if (mention["main"] != mention["mention"] and mainIdx != mentionStart and sentenceMention != sentenceIdx):
        docIdxStart = doc[mentionStart].idx
        docIdxEnd = doc[mentionEnd].idx + len(doc[mentionEnd])
        print(mention["mention"].start_char, mention["mention"].end_char, docIdxStart, docIdxEnd )
        print(docIdxStart, docIdxEnd, offset, len(mention["main"].text) )
        newDoc = newDoc[: docIdxStart+offset] + mention["main"].text + newDoc[ docIdxEnd + offset : ]
        offset = offset + (len(mention["main"].text) - (docIdxEnd - docIdxStart))

print(newDoc)



#
    #find main
    #Iterate through all mentions
    #Check if they are not in the same sentence or not main
    # replace





#text = text._.coref_resolved

segment_len = 50

sentenced_text = nltk.sent_tokenize(newDoc)
vocab = nltk.word_tokenize(newDoc)

vocab2 = list(dict.fromkeys(vocab))

print(sentenced_text)

vectors = [nlp(x).vector for x in vocab2]

wrdvecs = pd.DataFrame(vectors, index=vocab2)
vecr = CountVectorizer(vocabulary=wrdvecs.index)
sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)

print(sentence_vectors)


penalty = get_penalty([sentence_vectors], segment_len)
print('penalty %4.2f' % penalty)

optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=20)
segmented_text = get_segments(sentenced_text, optimal_segmentation)

print('%d sentences, %d segments, avg %4.2f sentences per segment' % (
    len(sentenced_text), len(segmented_text), len(sentenced_text) / len(segmented_text)))

for x in segmented_text:
    print(x)
