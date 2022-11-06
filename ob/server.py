from ob.api.app import create_app
from ob.containers.api import ApiContainer


app = create_app(container=ApiContainer())
