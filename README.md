# OntEnrich
Application for ontology enrichment through linking with DBpedia.

## Setup
```bash
pip install requirements.txt
```
or
```cmd
python -m pip install requirements.txt
```

## Usage
For enriching the ontology, first specify all the properties in the options.json file:

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

## License
MIT License. Copyright (c) 2018 Maxim Maltsev.
