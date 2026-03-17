# TraceTheory Package
# Import CLI only when needed to avoid circular imports

__version__ = "0.1.0"

def get_cli():
    """Get CLI command group"""
    from .cli import cli
    return cli

__all__ = ["get_cli"]