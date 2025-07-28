import pdb

import pandas as pd
import matplotlib.pyplot as plt

cam_name = 'St_Pierre_3'
f_execution_durations = 'execution_duration_resume.csv'

df = pd.read_csv(f_execution_durations)
print(df)
bathy_resolutions = [20, 15, 12, 10, 8, 6, 4]
# colors = ['firebrick', 'red', 'darkorange', 'gold', 'greenyellow', 'limegreen', 'green']
colors = ['red', 'darkorange', 'gold', 'greenyellow', 'green']
proj_imgs_resolutions = [1, 1.5, 2, 3, 4]

f, ax = plt.subplots(figsize=(22, 10))
ax.set_title(f'EXECUTION TIME OF BATHYMETRY CALCULATION AT {cam_name.upper()}', fontsize=18)
ax.grid(True)
for i, proj_imgs_resolution in enumerate(proj_imgs_resolutions):
    time_executions = []
    for r in bathy_resolutions:
        time_executions.append(df['bathy_grid_{bathy_resolution}m'.format(bathy_resolution=r)][i] / 60.0)
    ax.plot(bathy_resolutions, time_executions, 'o-', label=f'input image resolution: {proj_imgs_resolution} m',
            color=colors[i], )
ax.set_xlim([4, 20])
ax.set_xlabel('Bathymetry grid resolution (m)', fontsize=18)
ax.set_ylabel('Time execution (mn)', fontsize=18)
plt.legend(fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig('execution_time_of_bathymetry_calculation.png')
# plt.show()



