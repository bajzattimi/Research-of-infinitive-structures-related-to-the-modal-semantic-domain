import sys
from pathlib import Path
from re import compile as re_compile

from yamale import make_schema, make_data, validate, YamaleError


def load_and_validate(schema_fname, inp_data, strict=True):
    with open(schema_fname, encoding='UTF-8') as fh:
        schemafile_content = fh.read()
    config_schema = make_schema(content=schemafile_content)

    if isinstance(inp_data, (str, Path)):
        with open(inp_data, encoding='UTF-8') as fh:
            inp_data_str = fh.read()
    else:
        inp_data_str = inp_data.read()
    data = make_data(content=inp_data_str)

    try:
        validate(config_schema, data, strict)
    except YamaleError as e:
        for result in e.results:
            print('Error validating data {0} with {1}:'.format(result.data, result.schema), file=sys.stderr)
            for error in result.errors:
                print('', error, sep='\t', file=sys.stderr)
        exit(1)
    return data[0][0]


def parse_filter_params(inp_data):
    config = load_and_validate(Path(__file__).parent / 'filter_params_schema.yaml', inp_data)
    any_tok = []
    cur_tok = []
    for config_elem in config[0]['delete']:
        name = config_elem['name']
        value = re_compile(config_elem['value'])
        if config_elem['cond'] == 'any_tok':
            any_tok.append((name, config_elem['not'], value, config_elem['to_delete'], config_elem['field_name']))
        else:
            cur_tok.append((name, config_elem['not'], value, config_elem['to_delete'], config_elem['field_name']))

    subs_dict = config[1]['substitute']
    return any_tok, cur_tok, subs_dict


def cond_fun(not_value, regex, tok_field_val):
    # not_value XOR regex.search(tok[field_name])
    return (not_value and not regex.search(tok_field_val)) or (not not_value and regex.search(tok_field_val))


def filter_sentence(sent, any_tok, cur_tok, clause_str):
    delete_ex = False
    for tok in sent:
        for name, not_value, regex, to_delete, field_name in any_tok:
            curr_tok_field = tok.get(field_name)
            if curr_tok_field is not None and cond_fun(not_value, regex, curr_tok_field):
                if 'example' in to_delete:
                    print('INFO:', f'FILTERED SENT ({name})', clause_str, file=sys.stderr)
                    delete_ex = True
                    break
        else:  # Continue if the inner loop wasn't broken
            # Source: https://stackoverflow.com/questions/189645/how-can-i-break-out-of-multiple-loops/189685#189685
            for name, not_value, regex, to_delete, field_name in cur_tok:  # Delete matching fields for current token
                curr_tok_field = tok.get(field_name)
                if curr_tok_field is not None and cond_fun(not_value, regex, curr_tok_field):
                    for field in to_delete:
                        tok.pop(field, None)
            if len(tok) == 0:
                print('ERROR: NO FIELD LEFT FOR TOKEN!')
                exit(1)
            continue
        break  # Inner loop was broken, break the outer
    return delete_ex
