from distutils.core import setup

setup(
    name = 'simple-markov',
    version = '0.1.0',
    description = 'A simple library for manipulating markov chains',
    url = 'https://github.com/Mandragorian/simple-markov',
    author = 'Mandragorian & VHarisop',
    license = 'GPLv3',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Students',
        'Programming Language :: Python :: 3',
    ],
    packages = [
        'simple_markov',
        'simple_markov.drawing',
        'simple_markov.io'
    ],

    install_requires = [
        'numpy',
        'scipy',
        'matplotlib',
        'graphviz',
        'networkx'
    ]
)
