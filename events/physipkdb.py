"""
This helps in automating event addition

- Deepa 1/5/22 for PhysiPKPD
"""
from basico import *
from typing import Dict, List

# pandas configuration
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)


def get_experimental_indices(**kwargs):
    """
        my copy from basico
        This function  returns the exp idx for each dependent variable, with traces for all experiments.

        :param kwargs:

        - | `model`: to specify the data model to be used (if not specified
          | the one from :func:`.get_current_model` will be taken)

        :return: dict of (dependent variable, experimental indices)
        """
    dm = model_io.get_model_from_dict_or_default(kwargs)
    task = dm.getTask(TASK_PARAMETER_ESTIMATION)
    problem = task.getProblem()
    experiments = problem.getExperimentSet()
    result = []
    num_experiments = experiments.getExperimentCount()
    if num_experiments == 0:
        return result

    dependent_variables = {}
    experiment_names = {}
    for i in range(num_experiments):
        experiment = experiments.getExperiment(i)
        mapping = get_experiment_mapping(experiment)
        experiment_names[i] = experiment.getObjectName()

        # set independent values for that experiment
        independent = mapping[mapping.type == 'independent']
        xname = independent.iloc[0].mapping

        # set dependent values for that experiment
        dependent = mapping[mapping.type == 'dependent']
        num_dependent = dependent.shape[0]
        for j in range(num_dependent):
            name = dependent.iloc[j].mapping
            if name not in dependent_variables:
                dependent_variables[name] = []
            # contains the experimental indices for each dependent variable
            dependent_variables[name].append(i)

    return dependent_variables, experiment_names


def create_experiments(data_path):
    """
    :param remove_exp: bool
    :return:
    """
    df = pd.read_csv(data_path, sep="\t")
    df = df.dropna(axis=0, how='all')  # drop empty row
    mapping = {'drug1': 'drug1_c'}

    sids_all: List[str] = [sid for sid in df.columns]
    experiments: List[Dict] = []

    for i, exp_id in enumerate(df.experiment.unique()):
        exp: Dict = {}
        df_item = df[df.experiment == exp_id]
        index = df_item.index.to_list()
        exp['filename'] = str(data_path)

        if i == 0:
            exp['name'] = 'Experiment'
            exp['first_row'] = index[0] + 1

        else:
            exp['name'] = f'Experiment_{i}'
            exp['first_row'] = index[0] + 2

        exp['header_row'] = 1
        exp['last_row'] = index[-1] + 2
        exp['normalize_per_experiment'] = True
        exp['type'] = 'Time-Course'
        exp['weight_method'] = 'Mean Square'
        exp['separator'] = '\t'

        df_item = df_item.dropna(axis=1, how='all')  # drop empty columns
        sids: List[str] = [sid for sid in df_item.columns if sid not in ["dose_unit", "experiment"]]

        temp: List[Dict] = []
        for sid in sids_all:
            if sid == 'time':
                d = {'column': sid, 'type': 'time'}
            elif sid in sids:
                d = {'column': sid, 'object': mapping[sid], 'type': 'dependent'}
            else:
                d = {'column': sid, 'type': 'ignored'}
            temp.append(d)

        exp['mapping'] = temp
        experiments.append(exp)

    return experiments


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
    load_model(f)
    open_copasi(f)
