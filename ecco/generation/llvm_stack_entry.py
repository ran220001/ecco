from .llvm_value import LLVMValue


class LLVMStackEntry:
    def __init__(self, register, alignment_byte_amount):
        """
        Stores the information needed to place an element in the stack

        Args:
            register (LLVMValue): The register that the output of 'alloca' should be assigned to
            alignment_byte_amount (int): The number of bytes the output of the 'alloca' statement should be aligned with
                                         This is usually the width of the data type (e.g. 4 bytes for a 32-bit integer)
        """
        self.register = register
        self.alignment_byte_amount = alignment_byte_amount
