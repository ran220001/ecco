from ..ecco import GLOBAL_SCANNER
from .ecco_ast import ASTNode, new_ast_node
from ..scanning import Token, TokenType
from ..utils import EccoSyntaxError

OPERATOR_PRECEDENCE = {
    TokenType.PLUS: 4,
    TokenType.MINUS: 4,
    TokenType.STAR: 3,
    TokenType.SLASH: 3,
}


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
            f'Received "{str(GLOBAL_SCANNER.current_token.type)}" instead of terminal token'
        )


def parse_binary_expression(
    previous_token_precedence=max(OPERATOR_PRECEDENCE.values()) + 1,
):
    """
    Parses a binary expression using Pratt parsing

    Args:
        previous_token_precedence (int): The precedence of the previous token processed
                                         (is automatically set to
                                          the maximum possible operator precedence + 1
                                          if no tokens have been processed yet)

    Returns:
        An ASTNode containing the parsed binary expression
    """

    # Read an integer literal, then load the next token into GLOBAL_SCANNER.current_token
    left_term = parse_terminal_node()

    # Initialize variable node_type so it can be reused in the rest of the function
    node_type = GLOBAL_SCANNER.current_token.type

    # Return the last parsed node if end of file is reached
    if node_type == TokenType.EOF:
        return left_term

    """
    If the end of file has not been reached, it is assumed that the next node is an operator.
    This operator can be converted into an AST node
    whose children (leaf nodes) are either integer literals or other expressions.
    """

    # While the precedence of the current token is less than the precedence of the previously encountered token:
    while OPERATOR_PRECEDENCE[node_type] < previous_token_precedence:
        # Scan the next token
        GLOBAL_SCANNER.scan()

        # Next, parse the expression on the right (hooray, recursion!)
        right_term = parse_binary_expression(OPERATOR_PRECEDENCE[node_type])

        # Attach the expression tree on the right to the one we already have on the left
        left_term = ASTNode(Token(node_type), left_term, right_term)

        # Update the node type to ensure the while loop condition functions as intended
        node_type = GLOBAL_SCANNER.current_token.type

        # Check for end of file
        if node_type == TokenType.EOF:
            break

    return left_term
