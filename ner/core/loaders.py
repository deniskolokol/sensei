"""Loaders of NLP model."""

import os
import re
import pickle
import subprocess
from itertools import groupby

import tenacity
import nltk
import spacy
import spacy_udpipe
from spacy.matcher import Matcher
from spacy.attrs import POS

from sensei.ner.conf import settings


def ensure_nltk_data():
    nltk.download('stopwords')


def process_absent_spacy_model(spacy_model_name):
    """ download missing models """
    if spacy_model_name in settings.LANG_USING_UDPIPE:
        spacy_udpipe.download(spacy_model_name)  # download model
    else:
        # TOFIX: this will not work for PL model (currently all models
        # are downloaded in the Dockerfile)
        venv_path = os.environ.get('VIRTUAL_ENV', None)
        if venv_path:
            interpreter = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/python')
        else:
            interpreter = 'python'
        proc = subprocess.Popen([interpreter, '-m', 'spacy', 'download', spacy_model_name])
        proc.wait()


@tenacity.retry(stop=tenacity.stop_after_attempt(3))
def get_spacy_model(lang):
    """
    return spaCy model for a language (loeaded  in settings.SPACY_MODELS)
    or load model and return it
    or ask for downloading the model if it cannot be loaded
    """
    try:
        if lang not in settings.SPACY_MODELS:
            if lang in settings.LANG_USING_UDPIPE:
                settings.SPACY_MODELS[lang] = spacy_udpipe.load(lang)
            else:
                settings.SPACY_MODELS[lang] = spacy.load(settings.SPACY_LANG_MODEL[lang])
    except (OSError, Exception) as exc:
        process_absent_spacy_model(settings.SPACY_LANG_MODEL[lang])
        raise exc

    return settings.SPACY_MODELS[lang]


@tenacity.retry(stop=tenacity.stop_after_attempt(3))
def get_spacy_ner_model(lang):
    """
    similar to 'get_spacy_model' - returns the NER-specific spaCy model (stored in settings.SPACY_NER_MODELS)
    or loads model and return it
    or ask for downloading the model if it cannot be loaded
    """
    try:
        if lang not in settings.SPACY_NER_MODELS:
            settings.SPACY_NER_MODELS[lang] = spacy.load(settings.SPACY_NER_LANG_MODEL[lang])
    except OSError as exc:
        process_absent_spacy_model(settings.SPACY_NER_LANG_MODEL[lang])
        raise exc

    return settings.SPACY_NER_MODELS[lang]
