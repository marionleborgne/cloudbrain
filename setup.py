from setuptools import setup, find_packages
from pip.download import PipSession
from pip.req import parse_requirements
import os

# Get __version__ and set other constants.
exec(open(os.path.join('src', 'cloudbrain', 
                       'version.py')).read())
URL = 'https://github.com/cloudbrain/cloudbrain'
DOWNLOAD_URL='%s/archive/%s.tar.gz' % (URL, __version__)
DESCRIPTION = open('README.rst').read()

# Requirements
install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='cloudbrain',
      version=__version__,
      description='Platform for wearable data analysis.',
      author='Marion Le Borgne',
      author_email='marion@ebrain.io',
      url=URL,
      download_url=DOWNLOAD_URL,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=reqs,
      long_description=DESCRIPTION,
      test_suite='nose.collector',
      tests_require=['mock==1.0.1', 'nose'],
      include_package_data=True,
      package_data={
          "cloudbrain.core": ["*.json"],
          "cloudbrain.schema": ["*.json"]
      },
      extras_require={
          'muse:python_version>="3"': ['python-osc==1.6'],
      },
      entry_points = {
        'console_scripts':
            ['cloudbrain=cloudbrain.run:main']
        }
      )
