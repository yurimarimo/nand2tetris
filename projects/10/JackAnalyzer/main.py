import os
import sys
import glob
from compilationEngine import CompilationEngine

path = sys.argv[1]

if os.path.isfile(path):
  CompilationEngine(path, path.replace('.jack', '_yuriko.xml'))

elif os.path.isdir(path):
  if path[-1] != '/':
    path = path + '/'
  files = glob.glob(path + '*.jack')
  for file in files:
    CompilationEngine(file, file.replace('.jack', '_yuriko.xml'))

else:
  raise Exception('Error: Invalid path.')

