"""
This helps in automating event addition

version 0: event addition loadin + regular

- Deepa 1/5/22 for PhysiPKPD
"""
import pandas as pd
from basico import *
from typing import Dict, List
from pandas.errors import EmptyDataError

# pandas configuration
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)


def create_events_from_tc(data_path):
    """
    """
    if data_path.endswith('.csv'):
        sep = ","
    elif data_path.endswith('.tsv'):
        sep = "\t"

    try:
        df = pd.read_csv(data_path, sep=sep)
        df = df.dropna(axis=0, how='all')

        for index, row in df.iterrows():
            add_event(
                f'event_{index}',
                f'Time > {row["time"]}',
                [['drug1_c', f'[drug1_c] + {row["drug1"]}']]
            )

    except EmptyDataError:
        print(f"No dosing data in file: {data_path}")


if __name__ == '__main__':

    f = 'PK_dosing.cps'
    # -------------------------------------------------------------------------------------------------------------
    m = load_model(f)
    data_path = "dose_data.csv"
    set_species('drug1_c', initial_concentration=0, model=m)

    create_events_from_tc(data_path=data_path)
    # e = get_events()

    f = 'PK_dosing_check'
    save_model(f + '.xml', type='sbml')
    save_model(f + '.cps', type='copasi')
    load_model(f)
    open_copasi(f + '.cps')
