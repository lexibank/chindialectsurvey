from pathlib import Path

from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar
from clldutils.misc import slug

import attr
from pylexibank import Concept, Language
from pylexibank.forms import FormSpec


@attr.s
class CustomConcept(Concept):
    AlternativeName = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    DialectGroup = attr.ib(default=None)
    Location = attr.ib(default=None)
    Town = attr.ib(default=None)
    Speaker = attr.ib(default=None)
    Family = attr.ib(default='Sino-Tibetan')
    SubGroup = attr.ib(default="Kuki-Chin")
    LanguageName = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chindialectsurvey"

    # add your personalized data types here
    concept_class = CustomConcept
    language_class = CustomLanguage

    # define the way in which forms should be handled
    form_spec = FormSpec(
            brackets={"(": ")", '[': ']'},
            separators = ";/,",
            missing_data = ('?', '-', '0'),
            strip_inside_brackets=True
            )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        data = self.raw_dir.read_csv('wordlist.tsv', dicts=True, delimiter='\t')
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="ID")
        concepts = {}
        for concept in self.concepts:
            idx = concept['ID'].split('-')[-1] + '_' + slug(concept['ENGLISH'])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    AlternativeName=concept['AlternativeName'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS'],
                    )
            concepts[concept['ENGLISH']] = idx
        for row in progressbar(data, desc='cldfify'):
            if row['DOCULECT'] in languages:
                args.writer.add_forms_from_value(
                        Language_ID=row['DOCULECT'],
                        Parameter_ID=concepts[row['CONCEPT']],
                        Value=row['TRANSCRIPTION'],
                        Source=['chinds']
                        )



                    
