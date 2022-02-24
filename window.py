# from emtsv2 import analyse_input
with open('out_dep.tsv', encoding='UTF-8') as fh:
    for comment, sent in parse_emtsv_format(fh):
        print(comment)
        for tok in sent:
            pass  # print(tok)
        print()

# with open('out.tsv', encoding='UTF-8') as fh:
   # sent_iter = analyse_input(fh, keep_fields={'form', 'lemma', 'xpostag', 'upostag', 'feats', 'deprel', 'id', 'head'},
                             # modules=('morph', 'pos', 'conv-morph', 'dep'), server_name='http://emtsv.elte-dh.hu:5000')
   # for comment, sent in sent_iter:
       # print(comment)
       # for tok in sent:
           # pass  # print(tok)
        # print()
