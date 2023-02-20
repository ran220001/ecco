from ..ecco import GLOBAL_SCANNER
from ..ecco_ast import ASTNode, new_ast_node
from ..scanning import Token, TokenType
from ..utils import EccoSyntaxError


def parse_terminal_node():
    """
    Creates an AST node for the terminal node of the syntax tree

    Raises:
        EccoSyntaxError: If the terminal node being parsed is not an integer

    Returns:
        An AST node containing the parsed token
    """
    if GLOBAL_SCANNER.current_token.type == TokenType.INTEGER_LITERAL:
        output = new_ast_node(GLOBAL_SCANNER.current_token)
        GLOBAL_SCANNER.scan()
        return output
    else:
        raise EccoSyntaxError(
            f'Received "{str(GLOBAL_SCANNER.current_token.type)}" instead of terminal Token'
        )


def parse_binary_expression():
    # Read an integer literal, then load the next token into GLOBAL_SCANNER.current_token
    left_term = parse_terminal_node()

    # Return the last parsed node if end of file is reached
    if GLOBAL_SCANNER.current_token.type == TokenType.EOF:
        return left_term

    """
    If the end of file has not been reached, it is assumed that the next node is an operator.
    This operator can be converted into an AST node
    whose children (leaf nodes) are either integer literals or other expressions.
    """
    node_type = GLOBAL_SCANNER.current_token.type

    # Scan the next token
    GLOBAL_SCANNER.scan()

    # Next, parse the expression on the right (hooray, recursion!)
    right_term = parse_binary_expression()

    return ASTNode(Token(node_type), left_term, right_term)
