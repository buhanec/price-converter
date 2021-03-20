from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='price-converter',
    version='0.1.0',
    packages=find_packages(),
    author='Alen Buhanec <alen.buhanec@gmail.com>',
    license='MIT',
    description='A simple price conversion tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/buhanec/price-converter',
    entry_points={
        'console_scripts': ['priceconverter=priceconverter.tool:main'],
    },
    install_requires=['requests'],
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
)
