"""
from emtsv2 import analyse_input
with open('out.tsv', encoding='UTF-8') as fh:
   sent_iter = analyse_input(fh, keep_fields={'form', 'lemma', 'xpostag', 'upostag', 'feats', 'deprel', 'id', 'head'},
                             modules=('morph', 'pos', 'conv-morph', 'dep'), server_name='http://emtsv.elte-dh.hu:5000')
   for comment, sent in sent_iter:
       print(comment)
       for tok in sent:
           pass  # print(tok)
        print()
        """

from emtsv2 import parse_emtsv_format


def get_intValue_for_comment(i, key):
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


def main():
    with open('dep_out_tsv/mnsz_dep/akar_fni_384.tsv', encoding='UTF-8') as fh:
        for comment, sent in parse_emtsv_format(fh):
            print(comment)
            for i in comment:
                left_length = get_intValue_for_comment(i, 'left_length')
                if left_length is not None:
                    print(left_length)
            for tok in sent:
                pass  # print(tok)
            print()


if __name__ == '__main__':
    main()
