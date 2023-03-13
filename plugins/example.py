from app_data.state_manager import State
from app_data.plugin_loader import Plugin
import ctypes


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MousePlugin(Plugin):
    """A plugin that gets the mouse position"""

    name = "mouse"
    position = State((0, 0))

    def update(self):
        """Gets the mouse position"""
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        self.position = (pt.x, pt.y)

# plugin that logs the mouse position
class MousePosLogger(Plugin):
    def update(self, mouse_position):
        print(mouse_position)

def setup():
    return (MousePlugin(),)
