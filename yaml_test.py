import yaml
import re
with open('filter_tmk_to_emagyar.yaml', 'rb') as fh:
    y = yaml.safe_load(fh)
    re.compile(y['delete'][0]['value'])
