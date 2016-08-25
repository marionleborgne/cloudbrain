from setuptools import setup, find_packages
from pip.download import PipSession
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=PipSession())

reqs = [str(ir.req) for ir in install_reqs]


setup(name="cloudbrain",
      version="0.0.1",
      description="CloudBrain",
      author="Marion Le Borgne",
      url="https://github.com/cloudbrain/cloudbrain",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=reqs,
      license=open('LICENSE.txt').read(),
      long_description=open('README.md').read(),
      test_suite='nose.collector',
      tests_require=['mock==1.0.1', 'nose']
      )
