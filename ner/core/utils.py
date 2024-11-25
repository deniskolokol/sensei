import validators
from langdetect import detect

from genery.utils import TextCleaner


class NotFoundError(Exception):
    pass


def detect_lang(text):
    # Do not feed too big texts.
    def _do_detect(txt):
        txt = TextCleaner(txt).cleanup_hard()
        try:
            detector = Detector(txt)
        except Exception:
            return None
        return detector.language.code

    lim = 1000
    if len(text) <= lim:
        return _do_detect(text)

    curr = 100
    lang = None
    while (not lang) or (curr <= lim):
        lang = _do_detect(text[:curr])
        curr += 100

    return lang


class Paragraph:
    """Mimics some attributes of spaCy's Span class."""
    def __init__(self, text, start_char=None, end_char=None):
        self.text = text
        self.start_char = start_char or 0
        self.end_char = end_char or len(text)


def paragraphs(txt):
    """
    Generator that divides text to paragraphs.

    :param txt: <str> divided by '\n'. WARNING: if sentences in
                `txt` include '\n', this shoud be dealt with
                prior to call the generator (splitting text to
                sentences is dependent on lang).
    :yield: <class Paragraph> with attrs `txt` and `start_char`.
    """
    length = len(txt)
    start_char, end_char = 0, 0
    for par in txt.split('\n'):
        par_len = len(par)
        if par.isspace():
            # Ignore empty lines
            start_char += par_len
            end_char += par_len
            continue

        end_char += par_len
        try:
            while txt[end_char] != '\n':
                end_char += 1
        except IndexError:
            pass
        finally:
            # Count the last symbol '\n' in paragraph,
            # but don't exceed the length of the whole text.
            end_char += 1
            end_char = min(end_char, length)

        yield Paragraph(text=txt[start_char:end_char],
                        start_char=start_char,
                        end_char=end_char)

        start_char = end_char


def clean_text_to_paragraphs(text: str | list | tuple) -> list:
    assert isinstance(text, (str, list, tuple)), \
      TypeError(
            f"Parameter `text` is of wrong type: {type(text).__name__}! " + \
            "Only <str>, <list>, and <tuple> are allowed!"
            )
    if isinstance(text, (list, tuple)):
        return [x.strip() for x in text if x.strip()]

    return [x.text.strip() for x in paragraphs(text) if x.text.strip()]


def clean_text_flatten(text: str | list) -> str:
    return ' '.join(clean_text_to_paragraphs(text))


def clean_text(text: str | list, flatten: bool = False):
    if flatten:
        return ' '.join(clean_text_to_paragraphs(text))

    return clean_text_to_paragraphs(text)


def remove_urls(terms):
    """Remove URLs from the <list> of terms."""
    return [t.strip() for t in terms if not validators.url(t)]
