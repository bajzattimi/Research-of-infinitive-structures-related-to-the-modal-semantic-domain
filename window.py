from argparse import ArgumentParser, ArgumentTypeError


from emtsv2 import parse_emtsv_format


def get_int_value_for_fields_in_comment_lines(comment_lines, remaining_fields):
    fields = {}
    for comment_line in comment_lines:
        comment_line_splitted = comment_line.split(': ', maxsplit=1)
        key = comment_line_splitted[0]
        if key in remaining_fields and len(comment_line_splitted) == 2:
            value = comment_line_splitted[1]
            try:
                value_int = int(value)
            except ValueError as e:
                e.message = f'Cannot convert value ({value}) to int in comment line ({comment_line})!'
                raise
            fields[key] = value_int
            remaining_fields.discard(key)

            if len(remaining_fields) == 0:
                break
    else:
        raise ValueError(f'Some required fields ({remaining_fields}) not found in comment lines ({comment_lines})!')

    return fields


def get_int_value_for_tok_field(tok, field_name):
    value = tok.get(field_name)
    if value is None:
        raise ValueError(f'Field ({field_name} not in the available fields for token ({tok})!')
    try:
        value_int = int(value)
    except ValueError as e:
        e.message = f'Cannot convert value ({value}) to int in field ({field_name} for token ({tok})!'
        raise
    return value_int


def get_sent_parts(comment_lines, sent, left_window, right_window):
    fields = get_int_value_for_fields_in_comment_lines(comment_lines, {'left_length', 'kwic_length', 'right_length'})
    kwic_left = max(1, fields['left_length'] + 1 - left_window)
    kwic_right = min(len(sent), fields['left_length'] + 1 + fields['kwic_length'] + right_window)

    kwic_range = range(kwic_left, kwic_right)
    ranges = {range(1, kwic_left): 'left', kwic_range: 'kwic', range(kwic_right, len(sent)+1): 'right'}
    parts = {'left': [], 'kwic': [], 'right': [], 'left_new': [], 'kwic_new': [], 'right_new': []}

    for tok in sent:
        tokid_int = get_int_value_for_tok_field(tok, 'id')
        head_int = get_int_value_for_tok_field(tok, 'head')
        for sent_range, part in ranges.items():
            if tokid_int in sent_range:
                if head_int in kwic_range:
                    parts['kwic_new'].append(tok)
                else:
                    parts[f'{part}_new'].append(tok)
                parts[part].append(tok)
                break
        else:
            raise ValueError(f'{tok} does not appear in any range ({ranges})!')

    return parts


def create_window(inp_fh, left_window=3, right_window=3):  # TODO a process_one_file ezt hívja, ha megvan a file handle
    for comment_lines, sent in parse_emtsv_format(inp_fh):
        print('Original sent:', ' '.join(tok['form'] for tok in sent))
        sent_parts = get_sent_parts(comment_lines, sent, left_window, right_window)
        for kwic_type in ('kwic', 'kwic_new'):
            window = sent_parts[kwic_type]
            forms = [tok['form'] for tok in window]
            print('\t', f'{kwic_type}:', *forms)

def pars_args
if __name__ == '__main__':
    with open('dep_out_tsv/mnsz_dep/akar_fni_384.tsv', encoding='UTF-8') as fh:
        create_window(fh)

