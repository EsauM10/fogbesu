from typing import List
from fogbed import Container


def make_generate_blockchain_command(config_file: str, output_folder: str) -> str:
    command = 'besu operator generate-blockchain-config '
    command += f'--config-file={config_file} ' 
    command += f'--to={output_folder} '
    command += '--private-key-file-name=key'
    return command


def make_start_node_command(options: List[str] = []) -> str:
    return 'besu ' + ' '.join(options)


def get_enode_url(bootnode: Container) -> str:
    public_key = str(bootnode.environment['public_key'])
    id = public_key[2:]
    return f'enode://{id}@{bootnode.ip}:30303'


def read_config_file(filename: str) -> str:
    with open(filename, mode='r', encoding='utf-8') as file:
        return file.read()