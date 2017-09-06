from setuptools import setup, find_packages
from pip.download import PipSession
from pip.req import parse_requirements

VERSION = '0.0.8'
URL = 'https://github.com/cloudbrain/cloudbrain'
DOWNLOAD_URL='%s/archive/%s.tar.gz' % (URL, VERSION)

# Convert to RST if possible
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    license_description = pypandoc.convert('LICENSE.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
    license_description = open('LICENSE.txt').read()

# Requirements
install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='cloudbrain',
      version=VERSION,
      description='Platform for wearable data analysis.',
      author='Marion Le Borgne',
      author_email='marion@ebrain.io',
      url=URL,
      download_url=DOWNLOAD_URL,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=reqs,
      license=license_description,
      long_description=long_description,
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
            ['cloudbrain = cloudbrain.run']
        }
      )
