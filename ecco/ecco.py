from .scanning import Scanner, TokenType
from .utils import get_args, setup_tracebacks, EccoFatalException

DEBUG = True


def main():
    """Entry point for the compiler"""
    global GLOBAL_SCANNER
    args = get_args()

    GLOBAL_SCANNER = Scanner(args.PROGRAM)
    GLOBAL_SCANNER.open()
    setup_tracebacks()
    GLOBAL_SCANNER.scan()

    # The parse_binary_expression import is used to avoid "AttributeError: partially initialized module" errors with GLOBAL_SCANNER
    from .parsing import ASTNode, parse_binary_expression

    parsed_ast = parse_binary_expression()

    def interpret_ast(root_node):
        """
        Recursively steps through the AST and executes the operations on the nodes

        Args:
            root_node (ASTNode): Root node of the AST to be stepped through
        Raises:
            EccoFatalException: If the Token found is of an unknown (uninterpretable) type
        Returns:
            The value of the interpreted node of the tree
        """

        # Recursively interpret both sides of the root node (if they exist)
        if root_node.left:
            left_value = interpret_ast(root_node.left)
        if root_node.right:
            right_value = interpret_ast(root_node.right)

        if root_node.token.type == TokenType.INTEGER_LITERAL:
            return root_node.token.value
        elif root_node.token.type == TokenType.PLUS:
            return left_value + right_value
        elif root_node.token.type == TokenType.MINUS:
            return left_value - right_value
        elif root_node.token.type == TokenType.STAR:
            return left_value * right_value
        elif root_node.token.type == TokenType.SLASH:
            return (
                left_value // right_value
            )  # ECCO currently only handles integer division
        elif root_node.token.type == TokenType.LEFT_SHIFT:
            return left_value << right_value
        elif root_node.token.type == TokenType.RIGHT_SHIFT:
            return left_value >> right_value
        else:
            raise EccoFatalException(
                "FATAL", f"Unknown token encountered: {str(root_node.token.type)}"
            )

    print(interpret_ast(parsed_ast))

    GLOBAL_SCANNER.close()


if __name__ == "__main__":
    main()
