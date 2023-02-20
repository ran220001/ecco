# AST implementation

from .scanning import Token
from copy import deepcopy


class ASTNode:
    def __init__(self, source_token, left=None, right=None):
        """Creates an AST node from a given token"""

        self.token = deepcopy(source_token)

        # Set both left and right nodes to the passed values, then link them to the self as their parent
        self.left = left
        if self.left:
            self.left.parent = self
        self.right = right
        if self.right:
            self.right.parent = self

        # By default, a created node is a root node, so it has no parent
        self.parent = None


def new_ast_node(source_token):
    """Creates a new AST node with no children"""
    return ASTNode(source_token, None, None)


def new_unary_ast_node(source_token, child):
    """Creates a new AST node with only one child"""
    return ASTNode(source_token, child, None)
