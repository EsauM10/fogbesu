import json
from typing import Any, Dict, List
from fogbed import Container, VirtualInstance
from fogbed.experiment import Experiment

protocols = {
    'clique': 'CLIQUE', 
    'ibft2':  'IBFT', 
    'qbft':   'QBFT'
}

def create_topology(experiment: Experiment, network: Dict[VirtualInstance, List[str]]):
    for instance, hosts in network.items():
        for host in hosts:
            container = Container(host, dimage='besu:latest')
            experiment.add_docker(container, instance)


def get_consensus_protocol(config_file: Dict[str, Any]) -> str:
    for protocol in protocols:
        try:
            config_file['genesis']['config'][protocol]
            return protocols[protocol]
        except: pass
    return ''


def get_enode_url(bootnode: Container) -> str:
    public_key = str(bootnode.environment['public_key'])
    id = public_key[2:]
    return f'enode://{id}@{bootnode.ip}:30303'


def make_generate_blockchain_command(config_file: str, output_folder: str) -> str:
    command = 'besu operator generate-blockchain-config '
    command += f'--config-file={config_file} ' 
    command += f'--to={output_folder} '
    command += '--private-key-file-name=key'
    return command


def make_start_node_command(options: List[str] = []) -> str:
    return 'besu ' + ' '.join(options)


def read_config_file(filename: str) -> str:
    with open(filename, mode='r', encoding='utf-8') as file:
        return file.read()
    

def to_dict(json_data: str) -> Dict[str, Any]:
    return json.loads(json_data)

def to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data)