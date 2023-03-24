import argparse
import io
import os
from pathlib import Path
from typing import List

import pandas as pd
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser(description='Plotting from a csv file')
parser.add_argument('--fig_width', default=8, type=int, help='fig width')
parser.add_argument('--fig_height', default=4, type=int, help='fig height')
parser.add_argument(
    '--type', default='idling', choices=['idling', 'bar'], help='type of test')


PLOT_PARAMS = {
    'idling': ('Ug', 'If', 'Uf'),
    'bar': ('Qg', 'Uf'),
}


def input_path() -> List[str]:
    return input('Укажите путь к папке или csv файлу:\n')


def open_file(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep=';', decimal=',', header=1, index_col='time')


def plot_graph(
        df: pd.DataFrame, width: int, height: int, type: str
        ) -> io.BytesIO:
    _, ax = plt.subplots(figsize=(width, height))
    
    for line in PLOT_PARAMS[type]:
        ax.plot(df[line], label=line, lw=1)
    
    ax.legend()
    ax.set_ylabel('o.e.')
    ax.set_xlabel('t, c')
    ax.grid(which='major')
    ax.minorticks_on()
    ax.axhline(lw=0.6, color='#000000')

    pic = io.BytesIO()
    plt.savefig(pic, format='png', dpi=100)
    plt.close()
    pic.seek(0)

    return pic


def get_filenames(path: str) -> List[str]:
    if os.path.isdir(path):
        return sorted(Path(path).glob('**/*.csv'))
    if path.endswith(('.csv', '.CSV')):
        return [path]
    return input_path()


def main(files: list, width: int, height: int, type: str = 'idling') -> int:
    saved_count = 0

    for file in files:
        pic = plot_graph(open_file(str(file)), width, height, type)

        with open(f'{str(file).replace("csv", "png")}', 'wb') as f:
            try:
                f.write(pic.getbuffer())
                print(f'Saved {f.name}')
                saved_count += 1
            except OSError as err:
                print(repr(err))
    
    print(f'Total number of saved files: {saved_count}')
    return saved_count


if __name__ == '__main__':
    conf = parser.parse_args()

    width = conf.fig_width
    height = conf.fig_height
    type_ = conf.type

    path = input_path()
    files = get_filenames(path)

    main(files, width, height, type_)
