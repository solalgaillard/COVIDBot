'''
    Les thèmes sont définis par des poids sur des mots cibles et du nombre d'occurences
    (par classement) dans les clusters.
'''
TOPICS_ASSOCIATED_BY_WEIGHTS = [ {
            "name": ["symptom"],
            "values": [
                    {"word": "symptom", "weight": 1},
                    {"word": "respiratory", "weight": 1},
                    {"word": "tract", "weight": 1},
                    {"word": "severe", "weight": 1},
                    {"word": "stool", "weight": .6},
                    {"word": "laboratory", "weight": .4},
                ],
            },
            {
            "name": ["test"],
            "values": [
                    {"word": "test", "weight": 1},
                    {"word": "laboratory", "weight": 1},
                    {"word": "precaution", "weight": .5},
                    {"word": "cdc", "weight": .5},
                    {"word": "processing", "weight": .8},
                    {"word": "guidance", "weight": .3},
                    {"word": "specimen", "weight": .8},
                    {"word": "guideline", "weight": .3},
                    {"word": "infectious", "weight": .1},
                    {"word": "processing", "weight": .8},
                    {"word": "detectable", "weight": .7},
                ],
            },
            {
            "name": ["data"],
            "values": [
                    {"word": "number", "weight": 1},
                    {"word": "death", "weight": 1},
                    {"word": "case", "weight": 1},
                    {"word": "country", "weight": .5},
                    {"word": "record", "weight": 1},
                    {"word": "figure", "weight": 1},
                    {"word": "rate", "weight": 1},
                    {"word": "total", "weight": 1},
                    {"word": "toll", "weight": 1},
                    {"word": "percentage", "weight": .8},
                ],
            },
            {
            "name": ["vaccine", "treatment"],
            "values": [
                    {"word": "vaccine", "weight": 1},
                    {"word": "trial", "weight": 1},
                    {"word": "drug", "weight": .6},
                    {"word": "immune", "weight": .7},
                    {"word": "treatment", "weight": .6},
                    {"word": "antibody", "weight": .5},
                ],
            },
            {
                "name": ["material", "healthcare"],
                "values": [
                    {"word": "respirator", "weight": 1},
                    {"word": "patient", "weight": 1},
                    {"word": "n95", "weight": 1},
                    {"word": "procedure", "weight": .7},
                    {"word": "protection", "weight": .7},
                ],
            },
            {
                "name": ["travel", "flights", "airline"],
                "values": [
                    {"word": "travel", "weight": 1},
                    {"word": "transportation", "weight": 1},
                    {"word": "flight", "weight": 1},
                    {"word": "cruise", "weight": 1},
                    {"word": "crew", "weight": 1},
                    {"word": "traveler", "weight": 1},
                    {"word": "airline", "weight": 1},
                    {"word": "entry", "weight": 1},
                    {"word": "disembarkation", "weight": 1},
                ],
            },
            {
            "name": ["politics"],
                    "values": [
                    {"word": "government", "weight": .7},
                    {"word": "trump", "weight": 1},
                    {"word": "european", "weight": .8},
                    {"word": "leader", "weight": .5},
                    {"word": "us", "weight": .4},
                    {"word": "senate", "weight": 1},
                    {"word": "briefing", "weight": 1},
                    {"word": "official", "weight": .5},
                    {"word": "eu", "weight": .4},
                    {"word": "republican", "weight": 1},
                    {"word": "lockdown", "weight": .3},
                    {"word": "public", "weight": .3},
                    {"word": "mask", "weight": .2},
                    {"word": "country", "weight": .2},
                ]
            }
        ]