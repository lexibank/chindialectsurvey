from lingpy import *
from clldutils.misc import slug
from pyglottolog import api

glottolog = api.Glottolog('/home/mattis/data/datasets/glottolog/')

data = csv2list('raw.tsv', strip_lines=False)

header = data[0]
speakers = data[1]
branches = data[2]
languages = data[3]
isos = data[5]
locations = data[6]
towns = data[7]
varieties = data[8]
ltable = [['ID', 'Name', 'Language', 'SubGroup', 'ISO639P3code', 'Location',
    'Town', 'Speaker']]
ctable = [['ID', 'NUMBER', 'ENGLISH', 'AlternativeName']]
D = {0: ['doculect', 'concept', 'transcription']}
idx = 1
for i, line in enumerate(data[9:]):
    concept = line[5]
    alt_concept = line[-6]
    number = line[4]
    if number.isdigit():
        for j in range(6, len(header)-10):
            head = header[j]
            speaker = speakers[j].strip()
            branch = branches[j]
            language = languages[j]
            iso = isos[j]
            location = locations[j]
            town = towns[j]
            variety = varieties[j].strip()
            name = slug(variety, lowercase=False)+'-'+(speaker.strip('?') or 'A')
            if name and not name.startswith('-') :
                word = line[j].strip().replace(' or ', '/')
                if word and word != '-':
                    D[idx] = [name, concept, word]
                    idx += 1
                if i == 8:
                    ltable += [[name, variety, language, branch, iso, location,
                        town, speaker]]
        ctable += [[str(i+1), number, concept, alt_concept]]
wl = Wordlist(D)
wl.output('tsv', filename='wordlist', ignore='all', prettify=False)
with open('../etc/concepts.tsv', 'w') as f:
    for line in ctable:
        f.write('\t'.join(line)+'\n')
with open('../etc/languages.tsv', 'w') as f:
    for line in ltable:
        f.write('\t'.join(line)+'\n')
