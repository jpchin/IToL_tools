# IToL_tools
Tools for tree annotation with the Interactive Tree of Life.  

The purpose of this tool is to take a FASTA file which was used to create a taxonomic tree, parse the organism names from each sequence and compare this to a processed version of the NCBI taxonomic database.  It will then output a file compatible with the Interactive Tree of Life highlighting different taxonomic groups.

It consists of two scripts:

`taxDBTools.py` processes the NCBI taxonomic database into a parseable form.  It requires the `nodes.dmp` and `rankedlineage.dmp` files from NCBI's `new_taxdump` file [currently found here](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/).  This creates a single resource which is more simple to work with, and also "pads" the data to make it easier to search (see the `taxDBTools.py` script for more detail).  This *must* be run once, before the first attempt to use `IToL_Tools.py`, after which it shouldn't be necessary to run again unless NCBI make changes to their taxonomy files.

IToL_Tools.py takes an input multi FASTA file and extracts organism names by first looking for sequence start symbols (">") and then extracting everything on that line inside square brackets ("[" and "]").  It then performs a string search of the processed taxonomy database to find the NCBI taxID number of that organism.  It then backtracks through the processed database to construct an entire taxonomic lineage from whichever taxonomic level the sequence is from right back to the root of the NCBI taxonomy database.  During this process it will compile how many sequences are tracked to which taxonomic level, and give the user an option to select the desired level of taxonomy to be displayed on the IToL tree.  It will then output the text file necessary to make these annotations on the IToL website.



Very much a work in progress, not recommended for use by anyone right now.
