from typing import List

from flask_restx import Model

class Editor:
    def __init__(self, editor_id, name, address):
        self.editor_id = editor_id
        self.name = name
        self.address = address
        self.newspapers = []
        self.issues = []
    
    def update(self, name = None, address = None):
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
