from app_data.state_manager import State
from app_data.plugin_loader import Plugin

class TestPlugin(Plugin):
    name ='test'
    test_state = State('test_state')



def setup():
    return [TestPlugin()]
