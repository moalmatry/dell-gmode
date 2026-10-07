"""Dell G15 Fn+F9 G-Mode Performance Toggle Package."""
from .controller import GModeController
from .daemon import GModeDaemon

__version__ = "0.1.0"
__all__ = ["GModeController", "GModeDaemon"]
