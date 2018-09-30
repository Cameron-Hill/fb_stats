from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name='FacebookStatGenerator',
    version='0.4',
    description="A program that generates statistical summaries for provided facebook data",
    long_description=readme,
    packages=find_packages(),
    license="MIT",
    # url = ,
    install_requires=[
        'click >= 6.7',
        'pandas >= 0.23.3',
        'numpy >= 1.14.5'
    ],
    extras_require = {
        "Lemmatizer": ["nltk >= 3.3"],
        "Tests": ["beautifulsoup4>=4.6.3"]
    },
    entry_points={
        'console_scripts': [
            'fb_stats=fb_stats.cli:cli'
        ],
    },

)
