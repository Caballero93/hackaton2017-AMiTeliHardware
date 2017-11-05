"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from scipy.optimize import minimize




def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    # Dummy result is returned in every cycle here

    L1,L2,L3=True,True,True
    p_bat = 0.0
    panel=PVMode.ON
    if not msg.grid_status:
        temp=msg.solar_production+6-msg.current_load
        if temp<0:
            if temp>-0.3*msg.current_load:
                L3=False
            else:
                L2,L3=False,False
        if msg.bessSOC < 0.56:
            L3=False
        if msg.bessSOC < 0.2:
            L2,L3=False,False
        if msg.solar_production>msg.current_load and msg.bessSOC>0.99:
            panel=PVMode.OFF

    else:
        if msg.buying_price==3:
            if msg.bessSOC!=1:
                p_bat=-4.0
            else:
                p_bat=0.0
        else:
            if msg.current_load > 8.0:
                L2 = False
            if msg.solar_production < 0.3*msg.current_load:
                L3=False
            temp = msg.solar_production - msg.current_load
            if msg.selling_price==0:
                if( temp > 0):
                    p_bat=-temp
                else:
                    if temp > -4.0:
                        p_bat=-temp
                    else:
                        p_bat=4.0*msg.current_load/8
            else:
                if(temp > 0):
                    p_bat=0.0
                else:
                    if temp > -4.0:
                        p_bat=-temp
                    else:
                        p_bat=4.0*msg.current_load/8
                #p_bat=4.0



    if msg.bessSOC<0.2:
        if p_bat>0.0:
            p_bat=0.0


    return ResultsMessage(data_msg=msg,
                          load_one=L1,
                          load_two=L2,
                          load_three=L3,
                          power_reference =p_bat,
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
