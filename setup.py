import codecs
import os
from setuptools import find_packages, setup


# versioning should track against the api version
VERSION = '2.1.0'


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf8') as fh:
    long_description = fh.read()


setup(
    name='aot-client',
    version=VERSION,
    description='The Official Python Client of the Array of Things API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/UrbanCCD-UChicago/aot-client-py',
    author='Vince Forgione',
    author_email='vforgione@uchicago.edu',
    license='MIT',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(where='.', exclude=['tests', 'docs'])
)
