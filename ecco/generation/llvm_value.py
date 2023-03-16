from enum import Enum

from ..utils.ecco_logging import EccoInternalTypeError


class LLVMValueType(Enum):
    """A class to store the types of LLVMValues"""

    NONE = "LLVMValue (None)"

    VIRTUAL_REGISTER = "LLVMValue (Virtual Register)"

    # Return internal value upon casting to string
    def __str__(self):
        return self.value

    # Return index of value upon casting to integer
    def __int__(self):
        return LLVMValueType._member_names_.index(self._name_)


class LLVMValue:
    def __init__(self, llvm_value_type, stored_value):
        """
        Stores the data of a passed LLVM value

        Args:
            llvm_value_type (LLVMValueType): The type of the LLVM value to be stored
            stored_value: The value to be stored

        Raises:
            EccoInternalTypeError: If the value in stored_value is not an integer
        """
        self.value_type = llvm_value_type  # Store the info so that it can be accessed outside of the init function
        if llvm_value_type == LLVMValueType.VIRTUAL_REGISTER:
            if type(stored_value) != int:
                raise EccoInternalTypeError(
                    str(int),
                    str(type(stored_value)),
                    "generation/llvm_value.py:LLVMValue.__init__",
                )
            self.int_value = stored_value  # Store the info so that it can be accessed outside of the init function
            # Variable has been named int_value to conform with the pre-existing code in llvm.py

    def __repr__(self):
        if self.value_type == LLVMValueType.VIRTUAL_REGISTER:
            append_string = f": %{self.int_value}"
        else:
            append_string = ""
        return f"LLVMValue ({self.value_type})" + append_string
