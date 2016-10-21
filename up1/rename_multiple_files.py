import os
import glob
files = glob.glob('this*.jpg')
for file in files:
    os.rename(file, 'year_{}'.format(file.split('_')[1]))
