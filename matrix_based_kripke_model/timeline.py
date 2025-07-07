import numpy as np
from anytree import Node

from kripke_model import KripkeMatrix

class Timeline:
    def __init__(self, state: KripkeMatrix):
        self.state = Node(name=state)
    
    def branch(self, new_state: KripkeMatrix):
        Node(name=new_state, parent=self.state)