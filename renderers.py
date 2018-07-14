from collections import Counter
from itertools import chain
from operator import itemgetter

from termcolor import colored


def type_dict(ds):
    return {d['type']: d['text'] for d in ds}


class Field:
    def __init__(self, text, color=None, bgcolor=None, attrs=[]):
        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.attrs = attrs

    def __str__(self):
        try:
            bgcolor = 'on_' + self.bgcolor
        except TypeError:
            bgcolor = self.bgcolor
        return colored(self.text, self.color, bgcolor, attrs=self.attrs)


class Result(Field):
    def __init__(self, data):
        super().__init__(data['text'])


class Word(Field):
    def __init__(self, word, lex_cat, gram_feats):
        gram_feats = ' '.join(map(' '.join, gram_feats.values()))
        super().__init__(
            ', '.join([word, ' '.join([gram_feats, lex_cat])]),
            bgcolor='red',
        )


class Translation(Field):
    def __init__(self, text):
        super().__init__(text, bgcolor='cyan')


class Example:
    def __init__(self, pair):
        de, en = pair
        self.de = Field(de, bgcolor='green', attrs=['bold'])
        self.en = Field(en, bgcolor='green')

    def __str__(self):
        return '\n'.join(map(str, [self.de, self.en]))


class LexicalEntry:
    GRAM_FEATS = ['Gender', 'Subcategorization']

    def __init__(self, data):
        gram_feats = {gf: [] for gf in self.GRAM_FEATS}
        translations = Counter()
        examples = []

        for entry in reversed(data['entries']):
            gf_data = type_dict(entry.get('grammaticalFeatures', ''))
            for gf in self.GRAM_FEATS:
                v = gf_data.get(gf)
                if v is not None:
                    gram_feats[gf].append(v)

            for sense in reversed(entry['senses']):
                for translation in sense.get('translations', []):
                    translations[translation['text']] += 1

                for example in sense.get('examples', []):
                    de = example['text']
                    try:
                        trans = example['translations']
                    except KeyError:
                        continue
                    en = trans[0]['text']
                    examples.append((de, en))

        self.lex_cat = Word(data['text'], data['lexicalCategory'], gram_feats)
        self.translations = list(map(Translation, sorted(translations, key=translations.get, reverse=True)))
        self.examples = list(map(Example, examples))

    def __str__(self):
        return '\n'.join([str(self.lex_cat), ', '.join(map(str, self.translations)), '\n'.join(map(str, self.examples))])


class Search:
    def __init__(self, q, data):
        self.q = q
        self.data = data
        self.results = list(map(Result, data['results']))

    def __str__(self):
        return ', '.join(self.results)


class Entry:
    def __init__(self, q, data):
        self.q = q
        self.data = data
        lex_ents = map(itemgetter('lexicalEntries'), self.data['results'])
        lex_ents = chain.from_iterable(lex_ents)
        self.lex_ents = list(map(LexicalEntry, lex_ents))

    def __str__(self):
        return '\n'.join(map(str, self.lex_ents))
