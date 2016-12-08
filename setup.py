from setuptools import setup, find_packages

setup(
    name="nextf1race",
    version="0.1.3",
    packages=find_packages(exclude=['tests*']),

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', '*.rst'],
        'race_data': ['*.json'],
    },

    # metadata for upload to PyPI
    author="Will Skywalker",
    author_email="cxbats@gmail.com",
    description="A command tool to show where and when the next Formula 1 race is.",
    license="Apache 2.0",
    url="https://github.com/WillSkywalker/nextf1race",   # project home page, if any
    keywords='f1 race Formula One motorsport',

    entry_points = {
        'console_scripts': [
            'nextf1race = nextf1race.nextf1race:main',                  
        ],              
    },


    # could also include long_description, download_url, classifiers, etc.
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',        
    ],
)