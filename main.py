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