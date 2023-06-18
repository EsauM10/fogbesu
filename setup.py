from setuptools import setup, find_packages


setup(
    name="fogbesu",
    version="0.1.0",
    description='Plugin to build a private Besu blockchain in Fogbed.',
    long_description='Plugin to build a private Besu blockchain in Fogbed.',
    keywords=['networking', 'emulator', 'blockchain', 'Internet', 'dlt', 'besu', 'fog'],
    url='https://github.com/EsauM10/fogbesu',
    author='Esaú Mascarenhas',
    author_email='esaumasc@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python 3.8',
        'Topic :: System :: Emulators'
        'Operating System :: Ubunbu OS',
        'Blockchain :: Hyperledger Besu',
    ],
    install_requires = [
        'fogbed @ https://github.com/EsauM10/fogbed/tarball/main#egg=fogbed',
    ],
    packages=find_packages(),
    zip_safe=False
)