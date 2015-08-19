import os
from setuptools import setup, find_packages



def read(fname):
  """
  Utility function to read specified file.
  """
  path = os.path.join(os.path.dirname(__file__), fname)
  return open(path).read()



setup(name="cloudbrain",
      version="0.0",
      description="CloudBrain",
      packages=find_packages(),
      install_requires=['pika'],
      long_description=read("README.md"))
