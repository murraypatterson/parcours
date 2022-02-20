# parcours

PARsimonious CO-occURrenceS

Infer all possible assignments of ancestral states for a set of
characters in a phylogenetic tree, given extant states and a cost
matrix using Sankoff's algorithm, and then compute pairwise
correlation, as determined by (co-) occurrence patterns among
respective ancestral assignments.

## Citation

Brendan Smith, Cristian Navarro-Martinez, Rebecca Buonpane, S. Ashley
Byun\* and Murray Patterson\*. Correlated Evolution in the Small
Parsimony Framework. In the *17th International Symposium on
Bioinformatics Research and Applications (ISBRA, Shenzhen, China,
2021)*, volume 13064 of LNCS,
608--619. 2021. [doi:10.1007/978-3-030-91415-8_51](https://doi.org/10.1007/978-3-030-91415-8_51).


# how to run

First, make sure that you have Python3 and NumPy as well as the [ETE
Toolkit](http://etetoolkit.org/), and Multiset.  The latter three can be installed on
most systems via

    pip3 install numpy
    pip3 install ete3
    pip3 install multiset

respectively, if you have `pip`, or through Conda.  Once these
prerequisites are met, simply run the `parcours` executable to run the
tool.  For the full set of parameters of `parcours`, type

    ./parcours -h

# quick example

The easiest way to run `parcours` is through a config file.  Go to the
`example/` directory and type

    ../parcours -f config.csv

to generate the solution for a given instance: a phylogeny `tree.nh`,
a set of extant states `extant.csv` of some characters, and a cost
matrix `cost.csv`.  An ancestral reconstruction appears in
`output.csv`, while all possible ancestral reconstructions for each
character (of `extant.csv`) appears in `solutions/`.  Finally, all
events that happen in the tree for single characters appear in
`unit.csv`, while all events that happen for pairs of characters,
along with their correlation, appear in `pairwise.csv`.

For another example with more than two states, the example used in
Fig. 2 of [Clemente et al.,
2009](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2677398/) to
illustrate the structure that stores all parsimonious solutions, go to
the `clemente/` directory and type `../parcours -f config.csv`.  The
three solutions implied by Fig. 2 of the above article are then found
in the `solutions/` subdirectory.

# felid vocalizations

Go to the `felidae/` directory and type `../parcours -f config.csv` to
obtain pairwise correlations among 14 felid vocalizations in
`extant.csv` (Sunquist and Sunquist, 2002) within the phylogenetic
tree `felidae.nh` (Johnson et al., 2006) with Leopard and Jaguar
"swapped" (Figueiro et al.)
