from fogbed import (
    Container, FogbedExperiment
)
from fogbesu import BesuBlockchain

if(__name__=='__main__'):
    nodes = 4
    exp   = FogbedExperiment()
    besu  = BesuBlockchain(
        experiment=exp, 
        bootnode='node1', 
        config_file='ibftConfigFile.json'
    )
    
    besu1 = exp.add_virtual_instance('besu1')

    for i in range(nodes):
        exp.add_docker(
            container=Container(f'node{i+1}', dimage='besu:latest'),
            datacenter=besu1,
        )
    besu.run()