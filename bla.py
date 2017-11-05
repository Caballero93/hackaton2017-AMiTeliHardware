import json
from my_rating import get_physics_metrics
import sys
import os
import re
import time
from functools import partial
from configparser import ConfigParser
import pickle
from enum import Enum
import zmq
from typing import Tuple, Optional, List, Any
from hackathon.utils.utils import DataMessage, ResultsMessage, PVMode
from my_rating import get_physics_metrics
from hackathon.solution.solution import worker
import pickle
from typhoonANN import TyphoonANN, float_to_struct


# Open profile file
with open("data/profiles.json", 'r') as f:
    profile = json.load(f)

    file = open("./input_data.pickle", "rb")
    input_data = pickle.load(file)

    list_for_ANN = []

    ann = TyphoonANN()

    ann.load_weights()

    results = []
    ratings = []
    for data in input_data:
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
        list_for_ANN.append(ann_data)
        bla = worker(data)

        """ TODO: implementiraj ANN """
        izlaz_mreze_float = ann.run_iteration(ann_data)[0]

        izlaz_struct = float_to_struct(data, izlaz_mreze_float)

        results.append(data)
        rating = get_physics_metrics(data, bla)
        ratings.append(rating)
        # print("Energy mark: {}, Penal: {}".format(rating[0], rating[2]))

        # ann.ann_train(ann_data)

    ann.save_weights()

    print("Zavrsio turu")

