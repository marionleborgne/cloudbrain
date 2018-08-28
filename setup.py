from setuptools import setup, find_packages
try:
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements
try:
    from pip.download import PipSession
except ImportError:
    from pip._internal.download import PipSession
import os

# Get __version__ and set other constants.
# Source: https://stackoverflow.com/a/16084844
with open(os.path.join('src', 'cloudbrain', 'version.py'), 'r') as f:
    exec (f.read())
URL = 'https://github.com/cloudbrain/cloudbrain'
DOWNLOAD_URL = '%s/archive/%s.tar.gz' % (URL, __version__)
DESCRIPTION = open('README.rst').read()


# Helper function for requirements parsing by requirement type
def parse_reqs(req_type):
    reqs_file = os.path.join('requirements', '%s.txt' % req_type)
    install_reqs = parse_requirements(reqs_file, session=PipSession())
    reqs = [str(ir.req) for ir in install_reqs]
    return reqs


# Get requirements for all types
REQUIREMENT_TYPES = ['core', 'analytics', 'muse']
reqs = {req_type: parse_reqs(req_type) for req_type in REQUIREMENT_TYPES}

setup(name='cloudbrain',
      version=__version__,
      description='Platform for wearable data analysis.',
      author='Marion Le Borgne',
      author_email='marion@ebrain.io',
      url=URL,
      download_url=DOWNLOAD_URL,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=reqs['core'],
      long_description=DESCRIPTION,
      test_suite='nose.collector',
      include_package_data=True,
      package_data={
          "cloudbrain.core": ["*.json"],
          "cloudbrain.schema": ["*.json"]
      },
      extras_require={
          'muse:python_version>="3"': reqs['muse'],
          'analytics': reqs['analytics']
      },
      entry_points={
          'console_scripts':
              ['cloudbrain=cloudbrain.run:main']
      }
      )
