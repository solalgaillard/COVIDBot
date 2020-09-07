covid_bot scraps institutional and news website such as the nytimes, the guardian, the bbc or the CDC, and provides an AIML chatbot based on the content retrieved.

To install:
```sh
$ sudo apt install python3-pip
$ sudo apt-get install python3-venv
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip3 install -r requirements.txt
#Make sure last Chrome is installed, not chromium but chrome
```

To Launch, nothing easier, just run. If files have never been built, the process will be long.
```sh
$ ./covid_bot.py
```

You can alternatively, scrap new data and rebuild the bot or relaunch the AIML building process at any of the important stages.
Just be aware that modifying a previous building stage will force a rebuild of the following one all to the actual creation
of the bot.

###Here are the build options:

```sh
--build or -b
```
with :
1. `all`: Goes through all the stages of building the bot. Equivalent in practice to
`scrap`
2. `corefseg`: Used to resolve the coreference within the corpus, but results were not satisfactory so I don't resolve the coref. This still segments the articles in multiple parts easier to work with, remove overused or flagged sentences as well as the duplicates. This is a particularly slow operation
3. `model`: Rebuild the models that can be used to determine wether or not an entry is COVID related.
4. `covidentries`: Extract COVID related entries depending on model used (Logistic Regression or SVM)
5. `covidtopics`: Extract COVID themes with TF-IDF and KMeans.
6. `botbrain`: Build the AIML code

```sh
--model or -m
```
with :
1. `SVM`: Uses Support Vector Machine to extract COVID related entries (default, slower but more accurate)
2. `logreg`: Uses Logistic Regression to extract COVID related entries

```sh
--labeling or -l
```
with :
1. `an int`: Will export a file based on the scrapped entry with the number of entries to label passed on option. Open the xml file created and label the entries related or not to covid. The program will use this file for classification.

Be careful, this will overwrite any existing file used for labeling.


##Roadmap - closed issues:

    done - Get rid of jobs announcement subdomains
    done - Filter better remaining html tags, css inlining
    done - Save date -- This ensures that stale links gradually disappears
    done - Make sure than there is at least one element on the page or more than a certain amount of characters.
    done - Scrapper
        done - a - Understand why rules won't work and the filter is not applied
            done - # - regex preparsing relative path, not absolute
        done - b - Bread-width-first (see settings file)
        done - c - Kill all queued requests (might not be relevant anymore since I'm not following requests)
        done - d - Extract date for each article
        done - e - Limit scrapping to what is past three months

    done - Coreference extraction.
    done - Text Segmentation
    done - Automatize to get a small corpus to label
    done - Label data
    done - TF-IDF with Logistic Regression or SVM to isolate COVID - Labeled data 500
    done - TF-IDF then K-Means clustering on all corpus to get terms out
    done - Get topic name by the most used terms per cluster
    done - Generate one aiml file per topic
    done - Review structure of dictionnary for mapping
    done - Understand why one topic is not in the cluster list
    done - Add non-topics to bot

    done - Add Random Tag To centralize cue and Entities pattern as shown below
    done - Better way to find patterns(single nouns and no verbs?)
    done - Bring permutations within one loop and test code
    done - Save Brain of Chatbot
    done - Allow parameters to be passed to cmd line to isolate the different type of actions possible
        done - a - Scrap only the web
        done - b - Export Data for labelling - done
        done - c - Load - done
        done - d - Pass type model to recognize covid text - done
        done - f - generate aiml - done
        done - g - launch bot - done
        done - h - start-from-scratch - done
        done - i - save model - done
        done - j - load model - done

    done - Install locally webdriver / Check that the path works - done
    done - Rules for automatic path to driver - done
    done - Make Driver Path absolute - done
    done - Prepare proper packaging - done
    done - Paths must be resolved properly - done

    done - Make sure it can be deployed and built anywhere - done
        done - a - Check all Packages - done
        done - b - Check Environment - Envpath - done

    done - ADD QUIT TO AIML - done
    done - Test env on linux - done

    done - On Scrapper, writing to files need to be invoked only once - done
    done - Refactor all the code - done
    done - Silence nltk downloads
    done - Comment Code - done beisdes AIML part
    
##Roadmap - open issues:

        #TODO - Better strategy in generating AIML - done

    #TODO - 

    #TODO - BRING In A different strategy for extracting facts, One subject,, all other noun_chunks, objs

    #TODO GET RID OF TEXTACY

    #TODO Add also topic data to non-topic

    #TODO EXPORT TO AIML WITH NEW SYSTEM - done

    #TODO contractions and lemmatization on input

    #TODO - Patterns to take out

    #TODO - Provide Basic AIML Bot - today
    
        #TODO - Survey where data structures can be replaced by Pandas DataFrame
    #TODO - Survey Cluster technique
    #TODO - 5 - Develop Mecanism to flag answer when special authorized user is interacting with the bot
        #TODO - 5 - a - Need to be able to blacklist entry - (Put it in a dic, and rebuild AIML)
    #TODO - PIPE NLP when processing batches of docs for incredible speeding up
    #TODO - 2 - Cron Job to scrap and rebuild automatically the bot
    #TODO - 3 - Unit Testing
    #TODO - 4 - Word embeddings all across would have been more efficient than TF-IDF?
    #TODO - Investigate better Scrapping
        #TODO - c - Stupid meaningless sentences get kept
        #TODO - c - Investigate Paywall for NYT, do I need a new Login?

    #TODO - Label more Data and check between Logistic Regression and SVM which one is best

    #TODO - Review clustering process
