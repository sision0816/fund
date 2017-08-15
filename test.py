import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Create a random time series with values over 100 days
# starting from 1st March.
N = 100
dates = pd.date_range(start='2015-03-01', periods=N, freq='D')
ts = pd.DataFrame({'date': dates,
                   'values': np.random.randn(N)}).set_index('date')

# Create the plot and adjust x/y limits. The new x-axis
# ranges from mid-February till 1st July.
ax = ts.plot()
ts[0:30:10].plot(ax = ax)
# ax.set_xlim(pd.Timestamp('2015-02-15'), pd.Timestamp('2015-07-01'))
ax.set_ylim(-5, 5)
plt.show()
