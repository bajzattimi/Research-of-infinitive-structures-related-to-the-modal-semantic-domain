import sys
from pathlib import Path
from multiprocessing import Pool


def gen_input_output_filename_pairs(internal_fun, input_path, output_path, input_glob='*.tsv'):
    if Path(input_path).is_dir() and Path(output_path).is_dir():
        for inp_fname_w_path in Path(input_path).glob(input_glob):
            yield internal_fun, inp_fname_w_path, Path(output_path) / f'{inp_fname_w_path.stem}.tsv'
    elif ((input_path == '-' or Path(input_path).is_file()) and
          (output_path == '-' or not Path(output_path).is_dir())):  # The last is an existing or yet-to-be-created file
        yield internal_fun, input_path, output_path
    else:
        raise ValueError(f'Input and output must be both files (including STDIN/STDOUT) or directories'
                         f' ({(input_path, output_path)}) !')


MODE_PARAMS = {'text': (('r', {'encoding': 'UTF-8'}),
                        ('w', {'encoding': 'UTF-8'})),
               'binary': (('rb', {}),
                          ('wb', {}))}


def process_one_file(internal_fun, input_file, output_file, mode='text'):
    """
    Process a file into another file. Set *mode* to use binary files to avoid the encoding-decoidng overhead
    :param internal_fun: A partial fuction with preset parameters except input/output
    :param input_file: - for STDIN, filename or already opened file handle (for reading)
    :param output_file: - for STDOUT, filename or already opened file handle (for writing)
    :param mode: Either text or binary to represent reading/writing mode for input/output
    :return: Noting. Everything is written to output_file on success else exceptions are raised
    """
    mode_val = MODE_PARAMS.get(mode)
    if mode_val is None:
        raise ValueError(f'mode parameter ({mode}) can be either text or binary!')
    (read_mode, read_kwargs), (write_mode, write_kwargs) = mode_val

    close_inp_fh, close_out_fh = False, False
    if input_file == '-':
        inp_fh = sys.stdin
    elif isinstance(input_file, (str, Path)):
        inp_fh = open(input_file, read_mode, **read_kwargs)
        close_inp_fh = True
    elif hasattr(input_file, 'read'):
        inp_fh = input_file
    else:
        raise ValueError('Only STDIN, filename or file-like object is allowed as input !')

    if output_file == '-':
        out_fh = sys.stdout
    elif isinstance(output_file, (str, Path)):
        out_fh = open(output_file, write_mode, **write_kwargs)
        close_out_fh = True
    elif hasattr(output_file, 'writelines'):
        out_fh = output_file
    else:
        raise ValueError('Only STDOUT, filename or file-like object is allowed as output !')

    internal_fun(inp_fh, out_fh)

    # Without with statement we need to close opened files manually!
    if close_inp_fh:
        inp_fh.close()

    if close_out_fh:
        out_fh.close()


def process_one_by_one(gen_inp_out_fn_pairs, parallel=1, process_one_file_fun=process_one_file):
    if parallel > 1:
        with Pool(processes=parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file_fun, gen_inp_out_fn_pairs)
    else:
        for internal_fun, inp_fname_w_path, out_fname_w_path in gen_inp_out_fn_pairs:
            process_one_file_fun(internal_fun, inp_fname_w_path, out_fname_w_path)
