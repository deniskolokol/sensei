"""TextLib.project settings."""

import os
from logging import config

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Relative paths inside project directory
def rel(*x):
    return os.path.join(BASE_DIR, *x)


# Logging is pure console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': "[%(asctime)s %(levelname)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S %z",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
config.dictConfig(LOGGING)


# Project-wide
ENCODING = 'UTF-8'


# Communicaton.
NLP_SERVER_PORT = int(os.environ.get("NLP_SERVER_PORT", 80))


# Authentication.
NLP_TOKEN = os.environ.get("NLP_TOKEN", "")


# Default language.
LANG_DEFAULT = 'en'


# NLP features.
# NLTK data path.
NLTK_STOPWORDS_LANG = {
    'en': 'english'
    }
NLTK_DATA_PATH = rel('nlp', 'data', 'nltk')


LANG_USING_UDPIPE = ['sk', 'cs', 'fi', 'lv']

# Models are being loaded on demand...
SPACY_MODELS = {}
SPACY_NER_MODELS = {}

# spaCy lang model names.
# NB: for langs using spacy_udpipe the same as lang name (e.g. 'fi': 'fi')
SPACY_LANG_MODEL = {
    'en': 'en_core_web_sm',
    'sk': 'sk',
    'cs': 'cs',
    'pl' : 'pl_spacy_model',
    'el' : 'el_core_news_sm',
    'fi' : 'fi',
    'lv' : 'lv',
    'nl' : 'nl_core_news_sm',
    'it' : 'it_core_news_sm',
    'es' : 'es_core_news_sm'
}

VECTORIZER_LANG_DEF = {
    'en': {
        'spacy_pipeline': 'en_core_web_sm',
        'stop_words': 'english'
    },
    'de': {
        'spacy_pipeline': 'de_core_news_sm',
        'stop_words': 'german',
        'pos_pattern': '<ADJ.*>*<N.*>+'
    },
    'fr': {
        'spacy_pipeline': 'fr_core_news_sm',
        'stop_words': 'french',
    }
}


# General and specialized BERT models.
BERT_MODEL = {
    'ner': {
        'default': rel('nlp', 'data', 'bert-large-NER'),
        'd4data/biomedical-ner-all': rel('nlp', 'data', 'biomedical-ner-all'),
        'alvaroalon2/biobert_diseases_ner': rel('nlp', 'data', 'biobert_diseases_ner'),
        }
    }


# Maximum document size (symbols) for TextProcessor.
MAX_LENGTH_DEFAULT = int(os.environ.get("MAX_LENGTH_DEFAULT", 450_000))
