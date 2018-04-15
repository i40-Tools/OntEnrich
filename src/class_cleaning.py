from landscape import Ontology, DBpedia
import sys


def main(sto_path):
    ont = Ontology(sto_path)
    ont_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?sub ?type WHERE {
            ?sub rdf:type sto:Standard ;
                 rdf:type ?type .
        }
    """
    standard_classes = {}
    dbpcy_prefix = 'http://dbpedia.org/class/yago/'
    for row in ont.query(ont_query):
        standard_class = str(row[1])
        if standard_class[:len(dbpcy_prefix)] == dbpcy_prefix:
            standard_name = str(row[0])
            if standard_name not in standard_classes:
                standard_classes[standard_name] = [standard_class]
            else:
                standard_classes[standard_name].append(standard_class)
    #print(standard_classes)
    subclasses = []
    superclasses = []
    superclassof = {}
    for standard_name in standard_classes:
        classes_list = standard_classes[standard_name]
        for standard_class in classes_list:
            if standard_class not in subclasses:
                subclasses, superclasses, superclassof = extract_class(standard_class, subclasses, superclasses, superclassof)
    superclassof = extract_superclasses(superclassof)
    cnt = 0
    for standard_name in standard_classes:
        classes_list = standard_classes[standard_name]
        for standard_class in classes_list:
            if standard_class in superclasses or superclassof[standard_class] != 'http://dbpedia.org/class/yago/Abstraction100002137':
                ont.remove(standard_name, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', standard_class)
                cnt += 1
    print('Removed ' + str(cnt) + ' triples')
    ont.export('ttl/sto(clean).ttl')

def extract_superclasses(superclassof):
    for subclass in superclassof:
        while superclassof[subclass] in superclassof:
            superclassof[subclass] = superclassof[superclassof[subclass]]
    return superclassof

def extract_class(c, subclasses, superclasses, superclassof):
    dbpedia_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?superclass WHERE {
        <""" + c + """> rdfs:subClassOf ?superclass .
    }
    """
    dbpedia_result = DBpedia().query(dbpedia_query)
    if dbpedia_result:
        subclasses.append(c)
        superclass = dbpedia_result[0]['superclass']['value']
        superclassof[c] = superclass
        if superclass not in superclasses:
            superclasses.append(superclass)
    elif c not in superclasses:
        superclasses.append(c)
    return subclasses, superclasses, superclassof

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[2])
    else:
        print('ERROR: wrong number of arguments.')
