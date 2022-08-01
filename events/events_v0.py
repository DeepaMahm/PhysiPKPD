"""
This helps in automating event addition

version 0: event addition loadin + regular

- Deepa 1/5/22 for PhysiPKPD
"""
from basico import *
from typing import Dict, List

# pandas configuration
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)



def create_events_from_tc(data_path):
    """
    """
    df = pd.read_csv(data_path, sep="\t")
    df = df.dropna(axis=0, how='all')

    for index, row in df.iterrows():
        add_event(
            f'event_{index}',
            f'Time > {row["time"]}',
            [['drug1_c', f'[drug1_c] + {row["drug1"]}']]
        )

if __name__ == '__main__':

    f = 'PK_dosing.cps'
    # -------------------------------------------------------------------------------------------------------------
    m = load_model(f)
    data_path = "dose_data.tsv"
    create_events_from_tc(data_path=data_path)

    # experiments = create_experiments(data_path=data_path)
    # load_experiments_from_dict(experiments=experiments)  # removes all existing experiments

    e = get_events()
    f = 'PK_dosing_check.cps'
    save_model(f, type='sbml')
    save_model(f, type='copasi')
    load_model(f)
    open_copasi(f)
