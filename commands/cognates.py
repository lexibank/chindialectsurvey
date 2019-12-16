"""
Compute correspondence patterns from the data.
"""
import string
import pathlib

from lingpy.compare.partial import Partial
from lingpy import *

from lexibank_chindialectsurvey import Dataset

def run(args):
    ds = Dataset(args)
    wl = Wordlist.from_cldf(
            str(ds.cldf_specs().dir.joinpath('cldf-metadata.json')))
    D = {0: [x for x in wl.columns]}
    for idx in wl:
        if wl[idx, 'tokens']:
            D[idx] = wl[idx]
    part = Partial(D, check=True)
    part.get_partial_scorer(runs=10000)
    part.partial_cluster(method='lexstat', threshold=0.45, ref="cogids",
            cluster_method='infomap')
    alms = Alignments(part, ref='cogids', fuzzy=True)
    alms.align()
    alms.output('tsv', filename="chin-aligned")
