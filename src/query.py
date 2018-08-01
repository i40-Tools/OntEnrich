"""Module for enlarging existing ontology based on knowledge from DBpedia.
"""

from landscape import Ontology, DBpedia
import json
import sys
import csv

def main():
    """Main function.
    Describes abstract algorithm of the ontology enriching.
    """

    ont = Ontology('https://cdn.rawgit.com/i40-Tools/StandardOntology/semantic_lab/sto.ttl')
    ont_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?sub ?wiki ?dbp WHERE {
            ?sub rdf:type sto:Standard .
            ?sub sto:hasWikipediaArticle ?wiki .
            OPTIONAL { ?sub sto:hasDBpediaResource ?dbp } .
            FILTER ( !bound(?dbp) )
        }
    """
    print('...quering')
    reso_list = []
    for row in ont.query(ont_query):
        wiki = str(row[1])
        wiki = wiki.replace('https:', 'http:')
        dbp_query = '''
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?sub WHERE {
              ?sub foaf:isPrimaryTopicOf <''' + wiki + '''>
            }
        '''
        print(str(row[1]))
        dbp_result = DBpedia().query(dbp_query)
        dbp_resource = dbp_result[0]['sub']['value'] if len(dbp_result) > 0 else ''
        print('sto:hasDBpediaResource <' + dbp_resource + '>')
        reso_list.append([str(row[0]), str(row[1]), dbp_resource])
    with open('query/output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(reso_list)

if __name__ == "__main__":
    main()
