# OntEnrich
Application for knowledge graph enrichment through linking with DBpedia.

## Setup
```bash
pip install requirements.txt
```
or
```cmd
python -m pip install requirements.txt
```

## Usage
For enriching the ontology, first specify all the properties in the `options.json` file:

| Name | Description | Example |
| ---- | ----------- | ------- |
| input_file | Path to the ontology in .ttl fromat | `"ttl/sto.ttl"` |
| whitelist | List of predicates to fetch from DBpedia while enriching | `[ "<http://purl.org/dc/terms/subject>" ]` |
| blacklist | List of predicates to exclude from enrichment process | `[ "http://purl.org/voc/vrank#hasRank" ]` |
| prefixes | List of prefixes to assign to the resulting ontology | `[ { "prfx": "deo", "uri": "http://purl.org/spar/deo/" } ]` |

Next, execute `enrich.py` with `options.json` as a parameter:
```bash
python enrich.py options.json
```

## Example
Using a Turtle format of the [Standard Ontology (STO)](https://github.com/i40-Tools/StandardOntology) as an input without specifying `whitelist` and `blacklist` in the `options.json`, i.e., fetching all reachable data from [DBpedia](http://wiki.dbpedia.org/), the following results can be achieved:

| # of DBpedia links | # of added triples |
| ------------------ | ------------------ |
| 78 | 8268 |

You can check out the input and the resulting file [here](/examples).

## License
MIT License. Copyright (c) 2018 Maxim Maltsev.
