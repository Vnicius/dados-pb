import os

def createdir(path):
  try:
    os.mkdir(path)
  except:
    pass