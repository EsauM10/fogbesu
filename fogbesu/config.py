from typing import List
from fogbed import Container


class NodeKeys:
    def __init__(self, public: str, private: str) -> None:
        self.public = public
        self.private = private


class BlockchainConfigData:
    def __init__(self, bootnode: Container, output_folder: str) -> None:
        self.output_folder = output_folder
        self.genesis_file  = self._get_genesis_file(bootnode)
        self.keys = self._get_keys(bootnode)

    
    def _get_genesis_file(self, bootnode: Container):
        return bootnode.cmd(f'cat {self.output_folder}/genesis.json')
    
    def _get_keys(self, bootnode: Container) -> List[NodeKeys]:
        output = bootnode.cmd(f'ls {self.output_folder}/keys')
        directories = output.replace('\r', '').split('\n')
        directories.pop()
        
        return [
            NodeKeys(
                public=bootnode.cmd(f'cat {self.output_folder}/keys/{folder}/key.pub'),
                private=bootnode.cmd(f'cat {self.output_folder}/keys/{folder}/key')
            )
            for folder in directories
        ]
        