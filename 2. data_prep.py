import constants as cst
import pandas as pd
import os as os
import numpy as np
import random

from datetime import datetime

import imp
imp.reload(cst)

# Directories constant
DIR = cst.get_dirs()

# Read CSV
file_name = os.path.join(DIR['parent'], 'dhanushka_Fulldata_NYPD1.csv')
data = pd.read_csv (file_name)


# Rename Columns
data.columns = [
'DayOfWeek'
,'Day'
,'Month'
,'Year'
,'Time'
,'Location'
,'Ps_Injured'
,'Ps_Killed'
,'Ped_Injured'
,'Ped_Killed'
,'Cy_Injured'
,'Cy_Killed'
,'Mo_Injured'
,'Mo_Killed'
,'Vehicle_Group'
]



# Extract Hour
data['Time_Format'] = pd.to_datetime(data['Time'], format='%H:%M')
data['Hour'] = data['Time_Format'].dt.hour

# Target Variable
data['target'] = data.Ps_Injured + data.Ps_Killed + data.Ped_Injured + \
data.Ped_Killed + data.Cy_Injured + data.Cy_Killed + data.Mo_Injured + data.Mo_Killed
data['binary_target'] = np.where(data['target'] >= 1, 1, 0)

# Hour
data['Hour_00_03'] = np.where((data['Hour'] >= 0) & (data['Hour']  <= 3), 1, 0)
data['Hour_04_07'] = np.where((data['Hour'] >= 4) & (data['Hour']  <= 7), 1, 0)
data['Hour_08_11'] = np.where((data['Hour'] >= 8) & (data['Hour']  <= 11), 1, 0)
data['Hour_12_15'] = np.where((data['Hour'] >= 12) & (data['Hour']  <= 15), 1, 0)
data['Hour_16_19'] = np.where((data['Hour'] >= 16) & (data['Hour']  <= 19), 1, 0)
data['Hour_20_23'] = np.where((data['Hour'] >= 20) & (data['Hour']  <= 23), 1, 0)

data = pd.get_dummies(data, columns =["Month"])
data = pd.get_dummies(data, columns =["Location"])
data = pd.get_dummies(data, columns =["Vehicle_Group"])
data = pd.get_dummies(data, columns =["DayOfWeek"])

data.columns = data.columns.str.replace('\s+', '_')

# Drop all other variables
data = data.drop([
'Day'
,'Year'
,'Time'
,'Ps_Injured'
,'Ps_Killed'
,'Ped_Injured'
,'Ped_Killed'
,'Cy_Injured'
,'Cy_Killed'
,'Mo_Injured'
,'Mo_Killed'
, 'Time_Format'
, 'Hour'
, 'target'
], axis=1)

# split into train/dev/test
random.seed(1)

# Dev and test set each 10k rows
dev_and_test = random.sample(range(len(data)),20000)
dev = random.sample(dev_and_test, 10000)

data['partition'] = 'train'
data['partition'][dev_and_test] = 'test'
data['partition'][dev] = 'dev'

dev_set = data[data['partition'] == 'dev']
test_set = data[data['partition'] == 'test']

# Sanity check
sum(dev_set['binary_target'])
sum(test_set['binary_target'])

# Done, Export file
export_filename = os.path.join(DIR['parent'], 'clean_data.csv')
data.to_csv(export_filename, index = False)


