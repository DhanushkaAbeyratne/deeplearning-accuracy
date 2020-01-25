import constants as cst
import pandas as pd
import os as os

import seaborn as sns

import imp
imp.reload(cst)

# Directory Dictionary
DIR = cst.get_dirs()

# Load file
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



# Target Variable
data['target'] = data.Ps_Injured + data.Ps_Killed

#colours = sns.palplot(sns.color_palette("hls", 7))


# Example of Density Plots using Seaborn
# Please tweak as necessary.

alpha_level = 0.3

subset = data[['target', 'DayOfWeek']].query('DayOfWeek == "Mon"')
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Mon"')['target'],
                 shade = True, color = 'b', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Tue"')['target'],
                 shade = True, color = 'g', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Wed"')['target'],
                 shade = True, color = 'r', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Thu"')['target'],
                 shade = True, color = 'c', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Fri"')['target'],
                 shade = True, color = 'm', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Sat"')['target'],
                 shade = True, color = 'y', alpha = alpha_level, legend =False)
p1 = sns.kdeplot(data[['target', 'DayOfWeek']].query('DayOfWeek == "Sun"')['target'],
                 shade = True, color = 'k', alpha = alpha_level, legend =False)

# replace labels
p1.legend(['Mon', 'Tue','Wed','Thu','Fri','Sat','Sun'])
