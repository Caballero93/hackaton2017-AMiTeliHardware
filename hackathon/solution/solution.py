"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    # Dummy result is returned in every cycle here
    p_bat = 0.0

    if msg.buying_price == 8:
        load3 = False
    else:
        load3 = True

    if msg.grid_status:
        load1 = True
        load2 = True

        if msg.buying_price == 8:
            if msg.bessSOC > 0.6:
                p_bat = 6.0
            else:
                p_bat = 1.0
        else:
            p_bat = -6.0
    else:
        load1 = True
        load2 = True

    return ResultsMessage(data_msg=msg,
                          load_one=load1,
                          load_two=load2,
                          load_three=load3,
                          power_reference=float(p_bat),
                          pv_mode=PVMode.ON)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
