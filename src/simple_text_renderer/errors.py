class RendererIsUnknownError(TypeError):
    """Raised in case any renderer is not found for a provided block item."""


class DataIsMissingError(ValueError):
    """Raised in case user do not specify enough information to create a data object for a block."""
