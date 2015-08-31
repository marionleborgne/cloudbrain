import os
from setuptools import setup, find_packages



def read(fname):
  """
  Utility function to read specified file.
  """
  path = os.path.join(os.path.dirname(__file__), fname)
  return open(path).read()



setup(name="cloudbrain",
      version="0.2.0",
      description="Platform for real-time sensor data analysis and visualization.",
      packages=find_packages(),
      install_requires=['pika', 'pyliblo'],
      include_package_data=True,
      long_description=read("README.md"),
      license='GNU Affero General Public License v3',
      classifiers=[
          'License :: OSI Approved :: GNU Affero General Public License v3'
      ],
      entry_points = {
        'console_scripts': [
            'cloudbrain = cloudbrain.run:main'
        ]
      })
