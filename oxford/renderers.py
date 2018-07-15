from collections import Counter
from difflib import SequenceMatcher
from itertools import chain
from operator import itemgetter

from termcolor import colored


WIDTH = 80


def type_dict(ds):
    return {d['type']: d['text'] for d in ds}


class ReprMixin:
    repr_field = 'text'

    def __repr__(self):
        value = getattr(self, self.repr_field, None)
        return f'{self.__class__}: {value}'


class BGColor(ReprMixin):
    repr_field = 'raw'

    def __init__(self, raw_bgcolor=None):
        self.raw = raw_bgcolor

    @property
    def color(self):
        try:
            return 'on_' + self.raw
        except TypeError:
            return self.raw


class ColoredField(ReprMixin):
    repr_field = 'text'

    def __init__(self, text, color=None, bgcolor=None, attrs=[]):
        self.text = text
        self.color = color
        self.bg = BGColor(bgcolor)
        self.attrs = attrs

    def __str__(self):
        return colored(self.text, self.color, self.bg.color, attrs=self.attrs)


class ColoredFieldSet(ReprMixin):
    repr_field = 'fields'
    sep = ', '

    def __init__(self, fields, bgcolor=None):
        self.bgcolor = bgcolor
        for field in fields:
            if isinstance(field, ColoredField) and field.bg.color is None:
                field.bg.raw = bgcolor
        self.fields = fields

    def __str__(self):
        return self.color_sep.join(str(f) for f in self.fields)

    def __len__(self):
        return len(self.text)

    @property
    def text(self):
        return ' '.join(f.text for f in self.fields)

    @property
    def color_sep(self):
        if '\n' in self.sep:
            return self.sep
        return str(ColoredField(self.sep, bgcolor=self.bgcolor))


class ResultSet(ColoredFieldSet):
    def __init__(self, results):
        results = [ColoredField(f['word']) for f in results]
        super().__init__(results, bgcolor='red')


class Topline(ColoredFieldSet):
    def __init__(self, word, lex_cat, gram_feats):
        gram_feats = ' '.join(chain.from_iterable(gram_feats.values()))
        gram = f'{gram_feats} {lex_cat}' if gram_feats else lex_cat
        super().__init__(
            [ColoredField(word, attrs=['bold']), ColoredField(gram)],
            bgcolor='magenta',
        )


class TranslationSet(ColoredFieldSet):
    def __init__(self, fields):
        super().__init__([ColoredField(f) for f in fields], bgcolor='cyan')


class HighlightedExample(ColoredFieldSet):
    sep = ' '

    def __init__(self, text, word, **kwargs):
        sequence_matcher = SequenceMatcher()
        sequence_matcher.set_seq2(word)

        fields = []

        for w in text.split():
            extra_kwargs = {}

            sequence_matcher.set_seq1(w)
            if sequence_matcher.ratio() > 0.6:
                extra_kwargs['bgcolor'] = 'yellow'

            fields.append(ColoredField(w, **kwargs, **extra_kwargs))

        super().__init__(fields, bgcolor='green')


class ExampleSet(ColoredFieldSet):
    def __init__(self, pair, lexical_entry):
        de, en = pair
        super().__init__([
            HighlightedExample(de, lexical_entry.word, attrs=['bold']),
            ColoredField(en),
        ], bgcolor='green')

    @property
    def sep(self):
        return ' ' if len(self) < WIDTH else '\n'


class LexicalEntry(ReprMixin):
    repr_field = 'word'
    GRAM_FEATS = ['Gender', 'Subcategorization']

    def __init__(self, data):
        self.word = data['text']

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

        self.topline = Topline(self.word, data['lexicalCategory'], gram_feats)
        self.translation_set = TranslationSet(
            sorted(translations, key=translations.get, reverse=True)
        )
        self.example_sets = [ExampleSet(example, self) for example in examples]

    def __str__(self):
        return '\n'.join(map(
            str, [self.topline, self.translation_set] + self.example_sets)
        )


class Search:
    def __init__(self, data):
        self.data = data
        self.result_set = ResultSet(data['results'])

    def __str__(self):
        return str(self.result_set)


class Entry:
    def __init__(self, data):
        self.data = data
        lex_ents = map(itemgetter('lexicalEntries'), self.data['results'])
        lex_ents = chain.from_iterable(lex_ents)
        self.lex_ents = [LexicalEntry(lex_ent) for lex_ent in lex_ents]

    def __str__(self):
        return '\n\n'.join(map(str, self.lex_ents))
