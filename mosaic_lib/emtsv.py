import sys
from codecs import iterencode
from itertools import chain, repeat

from requests import post as requests_post, RequestException


class EMTSVRequestException(Exception):
    """A special exception to signal that the request has failed"""
    pass


def execute_request(input_iterator, modules=(), server_name='http://localhost:5000', conll_comments=True, retry=5,
                    decode_output=True):
    """
    Execute a request to an emtsv REST API from a file-like object input (raw text, or emtsv formatted text)
    :param input_iterator: a file-like object input (raw text, or emtsv formatted text)
    :param modules: The name of the modules to use
    :param server_name: The name of the emtsv server
    :param conll_comments: Keep CoNLL-style comments on output or not
    :param retry: The number of retries
    :param decode_output: Use the raw bytes as output or decode them to str
    :return: The iterator of the raw text/bytes output of emtsv by lines (line endings stripped)
    """
    if len(modules) == 0:
        raise ValueError(f'emtsv modules are empty: {modules} !')

    for i in range(1, retry+1):
        try:
            r = requests_post(f'{server_name}/{"/".join(modules)}', files={'file': input_iterator},
                              data={'conll_comments': conll_comments}, stream=True)
            if r.status_code != 200:
                print('emtsv error happened (try', i, '):', r.status_code, r.reason, file=sys.stderr)
            else:
                return r.iter_lines(decode_unicode=decode_output)
        except RequestException as e:
            print('Network error happened (retry', i, '):', e, file=sys.stderr)
    else:
        raise EMTSVRequestException(f'Could not process input: {input_iterator}')


def parse_emtsv_format(input_iterator, keep_fields=None):
    """
    Parse the emtsv raw format into a Python sturcture
     (iterator, sentences as lists, tokens as dicts, keys field names, values the token's properties)
    :param input_iterator: str iterator on lines of emtsv raw data
    :param keep_fields: list or set of field names to keep or None to keep all fields
    :return: iterator: sentences as lists, tokens as dicts, keys field names, values the token's properties
    """
    header = next(input_iterator, '')
    header_splitted = [col for col in header.rstrip('\n').split('\t') if len(col) > 0]
    # Check duplicate or empty fields in header!
    if header.count('\t') + 1 != len(set(header_splitted)):
        raise ValueError(f'Input header is not valid ({header_splitted}) !')

    header_filtered, len_header_filtered = header_splitted, len(header_splitted)
    if isinstance(keep_fields, list):  # Argparse returns list which must be cast to set
        keep_fields = set(keep_fields)
    if isinstance(keep_fields, set):
        header_filtered = []
        for col in header_splitted:
            if col in keep_fields:
                header_filtered.append(col)  # Fields to keep are denoted with their name
            else:
                header_filtered.append(None)  # Fields to omit are denoted with None

    comment, sent = [], []
    for i, line in enumerate(input_iterator, start=2):  # Header is already processed, the loop starts from the 2nd line
        line = line.rstrip('\n')
        if len(line) == 0:  # State 1: empty line (after sentences)
            yield comment, sent  # Yield the collected sentence and start a new empty one
            comment, sent = [], []
        elif line.startswith('# '):  # State 2: Comment, metadata
            comment.append(line[2:])  # Strip '# ' prefix and add the comments line by line withot further processing
        else:  # State 3: A line containing a token
            line_splitted = line.split('\t')  # Split to columns
            # Filter out columns not in keep_fields therefore denoted by None in header_filtered

            # zip(*_,strict=True) is available to raise ValueError in Python >=3.10
            if len_header_filtered != len(line_splitted):
                ValueError(f'For line {i} fields length ({len(line_splitted)}) does not match'
                           f' the length of the header ({len(header_splitted)}: {(header_splitted, line_splitted)} !',)

            # The others are put into a token dictionary with their field name as key
            token = {k: v for k, v in zip(header_filtered, line_splitted) if k is not None}
            sent.append(token)

    if len(comment) > 0 or len(sent) > 0:  # Yield all remaining tokens or metadata lines
        yield comment, sent


def format_emtsv_lines(it):
    """
    Format the input iterator of Python sturctured emtsv output into emtsv formatted lines
    :param it: The input iterator of Python sturctured emtsv output
    :return: Generator of emtsv formatted lines
    """
    tab = '\t'  # Store tab
    first_comment, first_sent = next(it)  # Can not be empty! All checks are performed in parse_emtsv_format()
    yield f'{tab.join(first_sent[0].keys())}\n'  # Header (in insertion order!)
    for comment, sent in chain([(first_comment, first_sent)], it):  # Push back first sentence into the iterator
        for comment_line in comment:
            yield f'#  {comment_line}\n'  # Write comment and add '# ' to the begining
        for token in sent:
            yield f'{tab.join(token.values())}\n'  # Write token (in insertion order!)
        yield '\n'  # Write empty line after sentences


def analyse_input(input_fh, output_fh=None, keep_fields=None, modules=(), server_name='http://localhost:5000',
                  conll_comments=True, retry=5):
    """
    Process a file handle into another file handle or to a python structured form as a geneator on sentences.
     Use binary files to avoid the encoding-decoidng overhead (applies only if no field filtering i.e. keep_fields=None)
    :param input_fh: An already opened file handle (for reading)
    :param output_fh: An already opened file handle (for writing) or None to return the generator
    :param keep_fields: The name of the fields to keep, None to keep all
    :param modules: The name of the modules to use
    :param server_name: The name of the emtsv server
    :param conll_comments: Keep CoNLL-style comments on output or not
    :param retry: The number of retries
    :return: The stentence generator where every token is a dict in a list (=sentence) for all sentences OR
             Noting. Writes output to output_fh
    """
    filter_fields = keep_fields is not None
    encoded_output_file = output_fh is not None and 'b' in output_fh.mode
    if encoded_output_file:
        decode_output = filter_fields  # Only have to decode if fileds need to be filtered
        newline = b'\n'  # Only used if there is no filtering, so it will not mess things up
    else:
        decode_output = True  # Must decode as output file is not binary
        newline = '\n'

    resp = execute_request(input_fh, modules, server_name, conll_comments, retry, decode_output)
    if output_fh is None:
        return parse_emtsv_format(resp, keep_fields)  # Return a sentence generator
    elif filter_fields:  # Filter to file output...
        resp = format_emtsv_lines(parse_emtsv_format(resp, keep_fields))
        if encoded_output_file:
            resp = iterencode(resp, 'UTF-8')  # Encode on the fly
    else:  # str/bytes to output file no filtering (just add newlines)
        resp = chain.from_iterable(zip(resp, repeat(newline)))  # Add newlines as str/bytes

    output_fh.writelines(resp)  # It actually writes an iterable only (not adding newlines)
