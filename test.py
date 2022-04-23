import pandas as pd
import numpy as np
from tqdm import tqdm

# Generate a dataframe with random numbers of shape 1,000 x 1,000
df = pd.DataFrame(np.random.randint(0, 100, (100000, 1000)))

# Register `pandas.progress_apply` with `tqdm`
tqdm.pandas(desc='Processing Dataframe')

# Add 3 to each value then cube for entire dataframe
df.progress_apply(lambda x: (x+3)**3)
print(df)