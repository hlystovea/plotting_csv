import argparse
import io
import os
from pathlib import Path
from typing import List

import pandas as pd
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Plotting from a csv file')
parser.add_argument('--fig_width', default=8, type=int, help='fig width')
parser.add_argument('--fig_heigth', default=4, type=int, help='fig height')
parser.add_argument(
    '--type', default='idling', choices=['idling', 'bar'], help='type of test')

PLOT_PARAMS = {
    'idling': ('Ug', 'If', 'Uf'),
    'bar': ('Qg', 'Uf'),
}


def input_path() -> List[str]:
    return check_path(input('Укажите путь к папке или csv файлу:\n'))

def open_file(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep=';', decimal=',', header=1, index_col='time')

def plot_graph(df: pd.DataFrame, conf: argparse.Namespace) -> io.BytesIO:
    _, ax = plt.subplots(figsize=(conf.fig_width, conf.fig_heigth))
    
    for line in PLOT_PARAMS[conf.type]:
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

def check_path(path: str) -> List[str]:
    if os.path.isdir(path):
        return sorted(Path(path).glob('**\\*.csv'))
    if path.endswith(('.csv', '.CSV')):
        return [path]
    return input_path()

if __name__ == '__main__':
    conf = parser.parse_args()

    num_files = 0
    files = input_path()

    for file in files:
        pic = plot_graph(open_file(str(file)), conf)
        with open(f'{str(file).replace("csv", "png")}', 'wb') as f:
            try:
                f.write(pic.getbuffer())
            except Exception as err:
                print(repr(err))
            else:
                print(f'Saved {f.name}')
                num_files += 1
    
    print(f'Total number of saved files: {num_files}')
