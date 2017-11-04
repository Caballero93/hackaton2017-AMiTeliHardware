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
    panel = PVMode.ON
    load1 = True
    load2 = True

    if msg.buying_price == 8 and msg.solar_production < 1:
        load3 = False
    else:
        load3 = True

    if msg.grid_status:
        # if msg.buying_price == 8 and msg.solar_production < 1 and msg.bessSOC < 0.3:
        #     load2 = False

        bla2 = msg.current_load * 0.5 if load2 else 0

        if msg.buying_price == 8:
            # if msg.current_load - bla2 > 8.5:
            #     load2 = False

            if msg.selling_price == 0:
                temp = msg.solar_production - msg.current_load + bla2
                if temp > 0:
                    p_bat = -temp
                else:
                    p_bat = 5 * msg.mainGridPower / 8
            else:
                p_bat = 5 * msg.mainGridPower / 8
        else:
            p_bat = -6.0
            if msg.solar_production > msg.current_load:
                p_bat -= msg.current_load - msg.solar_production
    else:
        load1 = True
        load2 = True
        load3 = True
        temp = msg.solar_production + 6 - msg.current_load
        if temp < 0:
            if temp > -0.3*msg.current_load:
                load3 = False
            else:
                load3, load2 = False, False

        if msg.bessSOC < 0.56:
            load3 = False
        if msg.bessSOC < 0.17:
            load3, load2 = False, False

        bla2 = msg.current_load * 0.5 if load2 else 0
        bla3 = msg.current_load * 0.3 if load3 else 0

        if (msg.solar_production > msg.current_load*0.2 + bla2 + bla3) and (msg.bessSOC > 0.99):
            panel = PVMode.OFF

    if msg.bessSOC < 0.192 and p_bat > 0:
        p_bat = 0.0

    # if msg.selling_price == 0 and msg.grid_status:
    #     p_bat = -2

    return ResultsMessage(data_msg=msg,
                          load_one=load1,
                          load_two=load2,
                          load_three=load3,
                          power_reference=float(p_bat),
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
