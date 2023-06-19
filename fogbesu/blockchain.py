import os
from typing import Dict, List

from fogbed import Container, Experiment, VirtualInstance

from fogbesu.config import BlockchainConfigData
from fogbesu.helpers import (
    create_topology,
    get_consensus_protocol,
    get_enode_url,
    make_generate_blockchain_command,
    make_start_node_command,
    read_config_file,
    to_dict,
    to_json,
)


BESU_DATA_PATH = '/tmp/besu'


class BesuBlockchain:
    def __init__(self, 
        experiment: Experiment, 
        config_file: str, 
        network: Dict[VirtualInstance, List[str]],
        bootnode: str = 'node1'
    ):
        self.exp = experiment
        self.bootnode_name = bootnode
        self.config_file   = to_dict(read_config_file(config_file))
        self.filename      = os.path.basename(config_file)
        self.network       = network
        self.output_folder = 'networkFiles'


    def get_host_allowlist(self, container: Container):
        return ','.join([
            host.ip
            for host in self.exp.get_containers()
            if(container != host)
        ])

    def configure_nodes(self, bootnode: Container):
        bootnode.ports.append(8545)
        bootnode.bindings.update({8545: 8545})
        consensus_protocol = get_consensus_protocol(self.config_file)

        for container in self.exp.get_containers():
            container.environment.update({
                'BESU_DATA_PATH': BESU_DATA_PATH,
                'BESU_RPC_HTTP_ENABLED': True,
                'BESU_RPC_HTTP_API': f'ETH,NET,PERM,{consensus_protocol}',
                'BESU_HOST_ALLOWLIST': '*',
                'BESU_RPC_HTTP_CORS_ORIGINS': 'all',
                'BESU_MIN_GAS_PRICE': 0})

    def clean_build_files(self, bootnode: Container):
        print('>> Cleaning bootnode build files... 🧹')
        bootnode.cmd(f'rm -rf {self.filename}')
        bootnode.cmd(f'rm -rf {self.output_folder}')
    
    def create_data_directories(self):
        print('>> Creating data directories... 📂')
        for node in self.exp.get_containers():
            node.cmd(f'mkdir {BESU_DATA_PATH} && cd {BESU_DATA_PATH}')

    def copy_config_file(self, bootnode: Container):
        print(f'>> Copying config file to bootnode ({self.bootnode_name})... 📤')
        data = to_json(self.config_file)
        bootnode.cmd(f"echo '{data}' >> {self.filename}")

    def copy_keys_to_nodes(self, config: BlockchainConfigData):
        nodes = self.exp.get_containers()
        for node, key in zip(nodes, config.keys):
            print(f'>> Copying keys to {node.name}... 📤')
            node.cmd(f"echo '{config.genesis_file}' >> {BESU_DATA_PATH}/genesis.json")
            node.cmd(f'echo {key.public} >> {BESU_DATA_PATH}/key.pub')
            node.cmd(f'echo {key.private} >> {BESU_DATA_PATH}/key')
            node.environment['public_key']  = key.public

    def generate_blockchain_config(self, bootnode: Container) -> BlockchainConfigData:
        print('>> Generating node keys... 🔑')
        command = make_generate_blockchain_command(self.filename, self.output_folder)
        bootnode.cmd(command)
        return BlockchainConfigData(bootnode, self.output_folder)


    def start_network(self, bootnode: Container):
        print(f'>> Starting {bootnode.name}... 🚀')
        command = make_start_node_command([
            f'--genesis-file={BESU_DATA_PATH}/genesis.json',
            f'--p2p-host={bootnode.ip} &'])
        bootnode.cmd(command)

        containers = self.exp.get_containers()
        containers.remove(bootnode)
        enode_url = get_enode_url(bootnode)

        for container in containers:
            print(f'>> Starting {container.name}... 🚀')
            command = make_start_node_command([
                f'--genesis-file={BESU_DATA_PATH}/genesis.json',
                f'--bootnodes={enode_url}',
                f'--p2p-host={container.ip} &'])
            container.cmd(command)
    

    def set_nodes_number(self, count: int):
        self.config_file['blockchain']['nodes']['count'] = count


    def run(self):
        print('>> Creating containers... 🛠️')
        create_topology(self.exp, self.network)
        bootnode = self.exp.get_docker(self.bootnode_name)
        self.configure_nodes(bootnode)
        self.set_nodes_number(count=len(self.exp.get_containers()))
        
        try:    
            self.exp.start()
            
            self.create_data_directories()
            self.copy_config_file(bootnode)
            config = self.generate_blockchain_config(bootnode)
            self.copy_keys_to_nodes(config)
            self.clean_build_files(bootnode)
            self.start_network(bootnode)
            input('Press any key to quit...')

        except Exception as ex:
            print(ex)
        finally:
            self.exp.stop()

