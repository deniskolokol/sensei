# -*- coding: utf-8 -*-

"""
Set of functions and classes that EXTRACT features from texts:
NER, keywords and keyphrases, etc.
"""
import logging
from string import punctuation

from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from transformers import AutoTokenizer, AutoModelForTokenClassification,\
     pipeline

from genery.utils import prepare_to_serialize, ensure_list

from nlp.utils import detect_lang, NotFoundError, clean_text
from nlp.models import Model


LOG = logging.getLogger('default')
LIMIT_KEYPHRASES = 100


def keyphrases(text: str, **kwargs) -> list:
    """
    Splits text to paragraphs (if necessary) and extract keyphrases
    along with cosine similarity (largest first).

    :param text: <str> or <list> of <str>

    :kwargs lang: <str>
    :kwargs flatten: <bool>, default False
    :kwargs topn: <int> default 10, max 1000.
        Warning: if flatten == True, the keyphrases from each paragraphs
          are combined and only `topn` distinct elements are returned.
          Otherwise (`flatten` default is False) `topn` elements for each
          paragraph are returned.
        Warning: there can be less than topn elements for a paragraph or
          the whole text, because there might not be that many keyphrases.

    :return: - if `flat == True`, <list> of <tuple>'s
             - otherwise <list> of <list>'s of <tuple> for each paragraph.
    """
    lang = kwargs.get('lang', None)
    if not lang:
        lang = detect_lang(text)
    if not lang:
        raise NotFoundError('Cannot detect language (maybe text too short?)')

    topn = kwargs.get('topn', 10)
    if topn > LIMIT_KEYPHRASES:
        LOG.warning('`topn` is above the limit of %d - the results will be cut!',
                    LIMIT_KEYPHRASES)
        topn = LIMIT_KEYPHRASES

    text = ensure_list(clean_text(text, kwargs.get('flatten', False)))

    kw_model = KeyBERT()
    kwargs_vect = Model().vectorizer.lookup(lang)
    # No kwargs for Vectorizer specific to the lang, use standard set.
    if not kwargs_vect:
        kwargs_vect = {}

    kwargs_vect.update({'lowercase': False})
    vectorizer = KeyphraseCountVectorizer(**kwargs_vect)
    result = kw_model.extract_keywords(docs=text,
                                       vectorizer=vectorizer,
                                       top_n=topn)
    return result[:topn]


def compile_entities(entities: list) -> list:
    """
    Compiling entities from IOB tagging to spaCy-like
    structure (for compatibility).
    """
    def prepare_word(word):
        word = word.strip()
        if word.startswith('#'):
            return word.replace('#', '')

        if word in punctuation:
            return word

        return  ' ' + word

    result = []
    current = {}

    for ent in entities:
        # entity == 0 is no entity, skip...
        if ent['entity'] == '0':
            # There can be unfinished `current` entity,
            # though - finalize & write to result.
            if current:
                result.append(current)
                current = {}
            continue

        if ent['entity'].startswith('B-'):
            if current:
                # Finalize & write current to result.
                result.append(current)
                current = {}

            ent_label = ent['entity'].split('-')[1]
            current = {
                "entity": ent['word'],
                "label": ent_label,
                "start_char": ent['start'],
                "end_char": ent['end']
                }
        else:
            # In some models entities start with 'I-', in which
            # cases `current` is an empty dict. This is clearly
            # a tagging problem, and should be omitted.
            try:
                current["entity"] += prepare_word(ent['word'])
            except KeyError:
                continue
            else:
                current.update({"end_char": ent['end']})

    return result


def prepare_entity(entity, text, model):
    # Inject model name.
    model_name = model.rsplit('/', 1)[-1]
    entity.update(model=model_name)

    # Fix entity text.
    entity['entity'] = text[entity['start_char']:entity['end_char']]

    return prepare_to_serialize(entity)


def named_entities(text: str, **kwargs) -> list:
    """
    Named Entity Recognizer.

    :kwarg model: <str> filename or id on huggingface.
    :kwarg raw: <bool> default False.
        If True, this will return the crude IOB-tagged output
        from BERT. Depending on the length of the text might
        sufficiently faster than a clean version. Used primarily
        for testing and fine-tuning.
    :return: <list> of <dicts>
    """
    model_name = kwargs.get('model', 'default')
    model = Model().get_bert_model(f'ner.{model_name}')
    if not model:
        model = Model().bert.ner.default

    tokenizer = AutoTokenizer.from_pretrained(model)
    model_ = AutoModelForTokenClassification.from_pretrained(model)
    nlp = pipeline('ner', model=model_, tokenizer=tokenizer)
    if kwargs.get('raw', False):
        entities = nlp(text)
    else:
        entities = compile_entities(nlp(text))

    return [prepare_entity(entity, text, model) for entity in entities]
