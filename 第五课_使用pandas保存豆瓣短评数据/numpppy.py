#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(6,3))
print(df.head())

df.to_csv('numpppy.csv')