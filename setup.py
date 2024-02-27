from setuptools import setup, find_packages

setup(
    name='arxivquery',
    version='1.0.3',
    author='Daniel Stamer-Squair',
    author_email='uaine.teine@hotmail.com',
    description='A simple wrapper for extracting Arxiv search results to a workable dataframe',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
