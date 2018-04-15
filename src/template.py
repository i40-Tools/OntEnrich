from landscape import Ontology, DBpedia
import json


def main():
    options = json.load(open('options.json'))
    prefixes = options['prefixes']
    template = json.load(open('template.json'))
    ont = Ontology('ttl/sto.ttl')
    ont_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?sub ?pred ?obj WHERE {
            ?sub rdf:type sto:Standard ;
                 ?pred ?obj .
        }
    """
    preds = {}
    logs = {}
    for row in ont.query(ont_query):
        raw_sub, raw_pred, raw_obj = row[0], row[1], row[2]
        sub, pred, obj = str(raw_sub), str(raw_pred), str(raw_obj)
        short_sub, short_pred, short_obj = get_shortcut(sub, prefixes), \
            get_shortcut(pred, prefixes), get_shortcut(obj, prefixes)
        # generate obj logs
        if short_sub not in logs:
            logs[short_sub] = []
        rdflib_types, prefix_types = get_types(template, pred)
        if rdflib_types:
            is_correct_type = ont.check_types(raw_obj, rdflib_types)
            if not is_correct_type:
                types_str = ' or '.join(rdflib_types)
                obj_type = type(raw_obj).__name__
                if obj_type == 'Literal':
                    log = short_pred + ' ' + obj + ' (type ' + obj_type + ', needed ' + types_str + ')'
                else:
                    log = short_pred + ' ' + short_obj + ' (type ' + obj_type + ', needed ' + types_str + ')'
                logs[short_sub].append(log)
        if prefix_types:
            is_correct_type = check_prefix_types(short_obj, prefix_types)
            if not is_correct_type:
                types_str = ' or '.join(prefix_types)
                obj_type = short_obj.split(':')[0]
                log = short_pred + ' ' + short_obj + ' (type ' + obj_type + ', needed ' + types_str + ')'
                logs[short_sub].append(log)
        # generate pred logs
        if short_sub not in preds:
            preds[short_sub] = []
        if pred not in preds[short_sub]:
            preds[short_sub].append(pred)
            if not rdflib_types:
                log = short_pred + ' is not specified in the templtate'
                logs[short_sub].append(log)
    logs = check_preds(logs, preds, template['necessary'], prefixes)
    save_logs(logs)

def get_types(template, pred):
    types_str = template['necessary'].get(pred) or template['useful'].get(pred) or \
            template['additional'].get(pred)
    rdflib_types = []
    prefix_types = []
    if types_str:
        types = types_str.split(', ')
        for obj_type in types:
            if obj_type == 'literal':
                rdflib_types.append('Literal')
            else:
                rdflib_types.append('URIRef')
            if obj_type.find('entity') > -1:
                prefix = obj_type.split('-')[0]
                prefix_types.append(prefix)
    return rdflib_types, prefix_types

def check_preds(logs, preds, template_necessary, prefixes):
    necessary_preds = []
    for pred in template_necessary:
        necessary_preds.append(pred)
    for sub in preds:
        tmp_necessaty_preds = necessary_preds.copy()
        for pred in preds[sub]:
            if pred in necessary_preds:
                tmp_necessaty_preds.remove(pred)
        if tmp_necessaty_preds:
            preds_short = []
            for pred in tmp_necessaty_preds:
                preds_short.append(get_shortcut(pred, prefixes))
            log = 'Lack of necessary predicates: [' + ', '.join(preds_short) + ']'
            logs[sub].append(log)
    return logs

def check_prefix_types(short_obj, prefix_types):
    for prefix in prefix_types:
        if short_obj.find(prefix) > -1:
            return True
    return False

def save_logs(logs):
    txt_logs = ''
    subs_with_logs_cnt = 0
    logs_cnt = 0
    for sub in logs:
        if logs[sub]:
            txt_logs += '\n'+ sub + '\n'
            for log in logs[sub]:
                txt_logs += '\t' + log + '\n'
                logs_cnt += 1
            subs_with_logs_cnt += 1
    head_log = 'Overall: ' + str(len(logs)) + ' standards analyzed, ' + \
      str(subs_with_logs_cnt) + ' standards can be improved, ' + \
      str(logs_cnt) + ' errors found.\n'
    txt_logs = head_log + txt_logs
    with open('template_logs.txt', 'w') as template_logs:
        template_logs.write(txt_logs)

def get_shortcut(uri, prefixes):
    for prefix in prefixes:
        uri = uri.replace(prefix['uri'], prefix['prfx'] + ':')
    return uri

if __name__ == '__main__':
    main()
