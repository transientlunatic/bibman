"""
Manage libraries.
"""

import os
import pathlib
import yaml

class Library:

    def __init__(self, root=os.getcwd()):

        with open(os.path.join(root, ".library", "library.yaml"), "r") as f:
            self.data = yaml.safe_load(f.read())

        self.root = root
            
        self.metadata = self.data['metadata']
        self.records = self.data['records']
    

    @classmethod
    def create(cls, name, root):
        pathlib.Path(root).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(root, ".library")).mkdir(parents=True, exist_ok=True)
        os.chdir(root)

        metadata = {}
    
        metadata["name"] = name

        with open(os.path.join(root, ".library", "library.yaml"), "w") as f:
            f.write(yaml.dump({'metadata': metadata, 'records': {}}))


    def _save(self):
        with open(os.path.join(self.root, ".library", "library.yaml"), "w") as f:
            f.write(yaml.dump({'metadata': self.metadata, 'records': self.records}))
            
    def add_record(self, record_object, download=True):
        """
        Add a new record to the library.
        """
        record_object.parse()
        self.records[record_object.record_id] = record_object.metadata

        if download:
            record_object.download_pdf(root=self.root)

        self._save()
