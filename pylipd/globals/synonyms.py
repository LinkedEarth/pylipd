import json
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SYNONYMS_FILE = DIR_PATH + "/synonyms.json"

with open(SYNONYMS_FILE, "r") as synfile:
    SYNONYMS = json.load(synfile)
    RSYNONYMS = {}
    for cat in SYNONYMS:
        for cls in SYNONYMS[cat]:
            synonyms = SYNONYMS[cat][cls]
            for syn in synonyms:
                synobj = synonyms[syn]
                RSYNONYMS[synobj["id"]] = synobj["label"]