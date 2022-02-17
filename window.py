from emtsv2 import analyse_input, parse_emtsv_format

# def analyse_input(input_fh, output_fh=None, keep_fields=None, modules=(), server_name='http://localhost:5000',
#                   conll_comments=True, retry=5):
with open('out.tsv', encoding='UTF-8') as fh:  # 'morph', 'pos'
    # TODO ez nem működik valamiért
    # sent_iter = analyse_input(fh, keep_fields={'form', 'lemma', 'xpostag', 'upostag', 'feats', 'deprel', 'id', 'head'},
    #                           modules=('conv-morph', 'dep'), server_name='http://emtsv.elte-dh.hu:5000')
    for comment, sent in parse_emtsv_format(fh):
        print(comment)
        for tok in sent:
            pass  # print(tok)
        print()
