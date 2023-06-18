# FogBesu
Plugin to enable the creation of a Hyperledger Besu blockchain using [Fogbed](https://larsid.github.io/fogbed/).

This package allows the creation of a private blockchain using [IBFT 2.0 or QBFT consensus protocols](https://besu.hyperledger.org/en/stable/private-networks/tutorials/ibft).

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
        config_file='configFile.json',
        network=network
    )
    blockchain.run()
```

## Distributed Blockchain
```py
from fogbed import FogbedDistributedExperiment
from fogbesu import BesuBlockchain


if(__name__=='__main__'):
    exp   = FogbedDistributedExperiment()
    besu1 = exp.add_virtual_instance('besu1')
    besu2 = exp.add_virtual_instance('besu2')

    worker1 = exp.add_worker(ip='192.168.0.150')
    worker2 = exp.add_worker(ip='192.168.0.151')

    worker1.add(besu1, reachable=True)
    worker2.add(besu2, reachable=True)
    exp.add_tunnel(worker1, worker2)

    network = {
        besu1: ['node1', 'node2'],
        besu2: ['node3', 'node4']
    }

    blockchain = BesuBlockchain(
        experiment=exp, 
        bootnode='node1', 
        config_file='configFile.json',
        network=network
    )
    blockchain.run()

```
Run a worker in each machine with `sudo RunWorker` and execute the script.
