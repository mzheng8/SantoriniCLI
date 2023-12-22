"""Exceptions for checking the validity of inputs"""
class InvalidSymbolError(Exception):
    """Indicates that the input was not a worker symbol"""
    pass

class InvalidWorkerError(Exception):
    """Indicates that the input was not the current player's worker"""
    pass

class CantMoveThereError(Exception):
    """Indicates all the errors for cells that can't be moved to"""
    pass

class CantBuildThereError(Exception):
    """Indicates all the errors for cells that can't be built on"""
    pass
