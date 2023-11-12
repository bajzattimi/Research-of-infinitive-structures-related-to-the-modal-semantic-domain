from pathlib import Path


def gen_input_output_filename_pairs(input_path, output_path, other_opts):
    if output_path != '-':
        output_path = Path(output_path)
        if len(output_path.suffixes) == 0 or output_path.is_file():
            raise ValueError(f'Output must be a file with extension and must not exist ({output_path}) !')
    if Path(input_path).is_dir():
        for inp_fname_w_path in Path(input_path).glob('*.tsv'):
            yield inp_fname_w_path, output_path, *other_opts
    elif input_path == '-' or Path(input_path).is_file():
        yield input_path, output_path, *other_opts
    else:
        raise ValueError(f'Input and output must be both files (including STDIN/STDOUT) or directories'
                         f' ({(input_path, output_path)}) !')
