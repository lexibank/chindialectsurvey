from pathlib import Path

from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb

# Customize your basic data
import attr
from pylexibank import Concept, Language

@attr.s
class NewConcept(Concept):
    AlternativeName = attr.ib(default=None)

@attr.s
class NewLanguage(Language):
    DialectGroup = attr.ib(default=None)
    ISO639P3code = attr.ib(default=None)
    Location = attr.ib(default=None)
    Language = attr.ib(default=None)
    Location = attr.ib(default=None)
    Town = attr.ib(default=None)
    Speaker = attr.ib(default=None)
    Family = attr.ib(default='Sino-Tibetan')
    SubGroup = attr.ib(default="Kuki-Chin")


#@attr.s
#class NewLexeme(Lexeme):
#    Attribute1 = attr.ib(default=None)
#    Attribute2 = attr.ib(default=None)

#@attr.s
#class NewCognate(Cognate):
#    Attribute1 = attr.ib(default=None)
#    Attribute2 = attr.ib(default=None)

# form specification
from pylexibank.forms import FormSpec

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chindialectsurvey"

    # add your personalized data types here
    concept_class = NewConcept
    language_class = NewLanguage

    # define the way in which forms should be handled
    form_spec = FormSpec(
            brackets={"(": ")", '[': ']'},
            separators = ";/,",
            missing_data = ('?', '-'),
            strip_inside_brackets=True
            )


    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        data = self.raw_dir.read_csv('wordlist.tsv', dicts=True, delimiter='\t')
        concepts = {}
        
        # short cut to add concepts and languages, provided your name spaces
        # match
        #args.writer.add_concepts()
        args.writer.add_languages()
        

        ## detailed way to do it
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept['ID'],
                    Name=concept['ENGLISH'],
                    AlternativeName=concept['AlternativeName'],
                    #Concepticon_ID=concept['CONCEPTICON_ID'],
                    )
            concepts[concept['ENGLISH']] = concept['ID']

        for row in pb(data, desc='cldfify'):
            args.writer.add_forms_from_value(
                    Language_ID=row['DOCULECT'],
                    Parameter_ID=concepts[row['CONCEPT']],
                    Value=row['TRANSCRIPTION'],
                    Source=[]
                    )



                    
