import os

from setuptools import find_packages, setup



def findRequirements():
  """
  Read the requirements.txt file and parse into requirements for setup's
  install_requirements option.
  """
  return [
    line.strip()
    for line in open("requirements.txt").readlines()
    if not line.startswith("#")
    ]



def read(fname):
  """
  Utility function to read specified file.
  """
  path = os.path.join(os.path.dirname(__file__), fname)
  return open(path).read()



setup(name="cloudbrain",
      version="0.2.1",
      description="Platform for wearable data analytics.",
      author="Marion Le Borgne",
      url="https://github.com/marionleborgne/cloudbrain",
      packages=find_packages(),
      install_requires=findRequirements(),
      include_package_data=True,
      long_description=read("README.md"),
      license='GNU Affero General Public License v3',
      classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3'
      ],
      entry_points={
        'console_scripts': [
          'cloudbrain = cloudbrain.run:main'
        ]
      })

