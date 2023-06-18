# FogBesu
Plugin to enable the creation of a Hyperledger Besu blockchain using Fogbed.

This package allows the creation of a private blockchain using [IBFT 2.0 consensus protocol](https://besu.hyperledger.org/en/stable/private-networks/tutorials/ibft).

## Install

#### 1. Install Containernet
```
sudo apt-get install ansible
```

```
git clone https://github.com/containernet/containernet.git
```

```
sudo ansible-playbook -i "localhost," -c local containernet/ansible/install.yml
```

#### 2. Install FogBesu
```
sudo pip install -U git+https://github.com/EsauM10/fogbesu.git
```

## Get Started
Copy the Dockerfile in this repository to build a compatible Fogbed Docker image and build it with:
```
sudo docker build -t besu .
```

Save the example below to a file and run with `sudo python3 example.py`.

```py
from fogbed import FogbedExperiment
from fogbesu import BesuBlockchain


if(__name__=='__main__'):
    exp   = FogbedExperiment()
    besu1 = exp.add_virtual_instance('besu1')

    network = {
        besu1: ['node1', 'node2', 'node3', 'node4', 'node5'],
    }

    blockchain = BesuBlockchain(
        experiment=exp, 
        bootnode='node1', 
        config_file='ibftConfigFile.json',
        network=network
    )
    blockchain.run()
```
