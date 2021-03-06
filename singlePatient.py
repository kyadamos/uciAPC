from simglucose.patient.t1dpatient import T1DPatient
from simglucose.simulation.sim_engine import SimObj, sim
from simglucose.sensor.cgm import CGMSensor, CGMNoise
from simglucose.actuator.pump import InsulinPump
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.simulation.scenario import Action, CustomScenario
from simglucose.simulation.env import T1DSimEnv
import plotBG
from controller import PController
from datetime import timedelta, datetime
import collections
import numpy as np
import matplotlib as plt
import pandas as pd

# patient setup
patientID = 12
patient = T1DPatient.withID(12)
sim_sensor = CGMSensor.withName('Dexcom')
sim_pump = InsulinPump.withName('Insulet')

# env setup
RANDOM_SEED = 5550
RUN_TIME = 48
sim_start_time = datetime(2020, 1, 1, 0,0,0)
sim_run_time =  timedelta(hours=RUN_TIME)

# random scenario
random_scen = RandomScenario(start_time = sim_start_time, seed = RANDOM_SEED)

# custom scenario
# meals is a list of tuples, each tuple containing a timedelta (time after start of sim) and a meal size, in g CHO.
meals = [(timedelta(hours=12), 100)]
# generate the custom scenario with the list of meals
custom_scen = CustomScenario(start_time = sim_start_time, scenario=meals)

# choose scenario
environment = T1DSimEnv(patient, sim_sensor, sim_pump, custom_scen)

# choose controller
controller = PController(gain = 0.04, dweight=.5, pweight=1, target=120)

# script saves csv(s) into this path
results_path = './results/'
simulator = SimObj(
    environment,
    controller,
    sim_run_time,
    animate=False,
    path = results_path
)
results = sim(simulator)
plotBG.group_plot(results, savedir='./results')