import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import pandas as pd

# upvotes and stuff
# df = pd.read_csv("../data/youtube_comments_clean.csv")
# upvotes = df['upvotes'].sum()
# print(upvotes)


# this is just a placeholder for now from: https://matplotlib.org/3.1.1/gallery/statistics/hist.html
# Fixing random state for reproducibility
np.random.seed(19680801)
N_points = 100000
n_bins = 20

# Generate a normal distribution, center at x=0 and y=5
x = np.random.randn(N_points)
y = .4 * x + np.random.randn(100000) + 5

fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# We can set the number of bins with the `bins` kwarg
axs[0].hist(x, bins=n_bins)
axs[1].hist(y, bins=n_bins)
filename = "test.png"
save = "../static/" + filename # to save the output and give it a name
fig.savefig(save) # saving the figure
#plt.show() # displaying it


