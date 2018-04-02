from landscape import Ontology, DBpedia
import pandas as pd


def main():
    ont = Ontology('examples/sto(enriched).ttl')
    ont_query_standard = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?sub ?pred ?obj WHERE {
            ?sub ?pred ?obj ;
                 rdf:type sto:Standard .
        }
    """
    standards = get_standards(ont.query(ont_query_standard))
    pair_same, pred_same, comm_same = get_similarities(standards)
    save(pair_same, 'same/pair_same.csv', ['pred', 'obj', 'cnt'])
    save(pred_same, 'same/pred_same.csv', ['pred', 'cnt'])
    save(comm_same, 'same/comm_same.csv', ['comm', 'cnt'])


def get_standards(query_result):
    standards = {}
    sto_prefix = 'https://w3id.org/i40/sto#'
    for row in query_result:
        st_name = str(row[0])[len(sto_prefix):]
        if st_name not in standards:
            standards[st_name] = []
        st_pred = str(row[1])
        st_obj = str(row[2])
        standards[st_name].append((st_pred, st_obj))
    print('number of standards =', len(standards))
    return standards


def get_similarities(standards):
    pair_same = {}
    pred_same = {}
    comm_same = {}
    rdfs_comment = 'http://www.w3.org/2000/01/rdf-schema#comment'
    for standard in standards:
        for tuple in standards[standard]:
            pred = tuple[0]
            pair = tuple[0] + '; ' + tuple[1]
            # Handling predicates
            if pred not in pred_same:
                pred_same[pred] = []
                pred_same[pred].append(standard)
            elif standard not in pred_same[pred]:
                pred_same[pred].append(standard)
            # Handling rdfs:comment
            if pred == rdfs_comment:
                comment = tuple[1]
                for punct in ['.', ',', ':', ';', '/', '(', ')','"']:
                    comment = comment.replace(punct, '')
                comment_list = comment.split(' ')
                for raw_word in comment_list:
                    word = raw_word.lower()
                    if word not in comm_same:
                        comm_same[word] = []
                        comm_same[word].append(standard)
                    elif standard not in comm_same[word]:
                        comm_same[word].append(standard)
                continue
            # Handling pairs predicate; object
            if pair not in pair_same:
                pair_same[pair] = []
                pair_same[pair].append(standard)
            elif standard not in pair_same[pair]:
                pair_same[pair].append(standard)
    return pair_same, pred_same, comm_same

def save(obj, file_name, df_columns):
    arr_to_write = []
    for key in obj:
        if key != '':
            # Generating columns for csv
            csv_line = key.split('; ')
            csv_line.append(len(obj[key]))
            arr_to_write.append(csv_line)
    # Converting to pandas DataFrame for saving as csv
    df = pd.DataFrame(arr_to_write, columns=df_columns)
    df.sort_values(by='cnt', inplace=True, ascending=False)
    df.to_csv(file_name, index=False, sep=',')
    print('calculations exported as', file_name)


if __name__ == '__main__':
    main()
