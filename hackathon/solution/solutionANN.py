"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from typhoonANN import TyphoonANN, float_to_struct


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    # Dummy result is returned in every cycle here
    ann = TyphoonANN()

    ann.load_weights()

    data = msg
    overload = float(1 if data.bessOverload else 0)
    ann_data = [overload,
                float(data.bessPower),
                float(data.bessSOC),
                float(data.buying_price),
                float(data.current_load),
                float(data.grid_status),
                float(data.mainGridPower),
                float(data.selling_price),
                float(data.solar_production)]

    izlaz_mreze_float = ann.run_iteration(ann_data)[0]

    bla = float_to_struct(data, izlaz_mreze_float)

    return bla


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
