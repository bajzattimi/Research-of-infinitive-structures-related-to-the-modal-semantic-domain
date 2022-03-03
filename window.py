from itertools import chain

from emtsv2 import parse_emtsv_format


def get_int_value_for_comment(i, key):
    if key in i:
        left_length = i.split(": ")
        if len(left_length) != 2:
            raise ValueError("TODO")  # (TODO Értelmes hibaüzenet)
        left_length = left_length[1]
        try:
            left_length_int = int(left_length)
        except ValueError as e:
            e.message = "TODO"  # (TODO Értelmes hibaüzenet)
            raise
        return left_length_int


def main(left_window=3, right_window=3):
    with open('dep_out_tsv/mnsz_dep/akar_fni_384.tsv', encoding='UTF-8') as fh:
        for comment_lines, sent in parse_emtsv_format(fh):
            sent_parts = get_sent_parts(comment_lines, sent, left_window, right_window)
            window = sent_parts['kwic']
            forms = [tok['form'] for tok in window]
            print(' '.join(tok['form'] for tok in sent))
            print('\t', *forms)


def get_sent_parts(comment_lines, sent, left_window, right_window):
    fields = {'left_length': None, 'kwic_length': None, 'right_length': None}
    for comment_line in comment_lines:
        for field_name, field_value in fields.items():
            if field_value is None:
                fields[field_name] = get_int_value_for_comment(comment_line, field_name)
    if any(e is None for e in fields.values()):
        raise ValueError('TODO')  # (TODO Értelmes hibaüzenet)
    parts = {'left': [], 'kwic': [], 'right': []}
    kwic_left = max(1, fields['left_length'] + 1 - left_window)
    kwic_right = min(len(sent), fields['left_length'] + 1 + fields['kwic_length'] + right_window)
    ranges = {range(1, kwic_left): 'left',
              range(kwic_left, kwic_right): 'kwic',
              range(kwic_right, len(sent)+1): 'right'}
    points_to = {}
    kwic_ids = set()
    for tokind, tok in enumerate(sent):
        tokid_int = get_int_value_for_tok_field(tok, 'id')
        head_int = get_int_value_for_tok_field(tok, 'head')
        points_to[head_int] = (tokid_int, tokind)
        for sent_range, part in ranges.items():
            if tokid_int in sent_range:
                parts[part].append(tok)
                if part == 'kwic':
                    kwic_ids.add(tokid_int)
                break
        else:
            raise ValueError(f'{tok} does not appear in any range ({ranges})')  # (TODO Értelmes hibaüzenet)
    extra_left, new_left = [], []
    for tok in parts['left']:
        head_int = get_int_value_for_tok_field(tok, 'head')
        if head_int in kwic_ids:
            extra_left.append(tok)
        else:
            new_left.append(tok)

    extra_right, new_right = [], []
    for tok in parts['right']:
        head_int = get_int_value_for_tok_field(tok, 'head')
        if head_int in kwic_ids:
            extra_right.append(tok)
        else:
            new_right.append(tok)

    """
    parts['left'] = new_left
    parts['right'] = new_right
    parts['kwic'] = list(chain(extra_left, parts['kwic'], extra_right))
    """

    return parts


def get_int_value_for_tok_field(tok, field_name):
    value = tok.get(field_name)
    if value is None:
        raise ValueError('TODO')  # (TODO Értelmes hibaüzenet)
    try:
        value_int = int(value)
    except ValueError as e:
        e.message = "TODO"  # (TODO Értelmes hibaüzenet)
        raise
    return value_int


if __name__ == '__main__':
    main()
