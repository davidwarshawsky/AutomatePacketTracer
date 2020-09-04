from src.router import Router
import os
class Network(object):

    def __init__(self,name):
        routers: [Router] = None
        self.path: str = '../networks'
        # Set the network name.
        self.name = name
        self.path = self.name

    @property
    def path(self):
        # Get the network path
        return self._path

    @path.setter
    def path(self,path):
        # If this is the first time setting the path, create a new
        # directory for the network.
        start_path = '../networks'
        if self._path == 'networks':
            self._path = os.path.join(self._path,path)
            if not os.path.isdir(self._path):
                os.mkdir(self._path)
        else:
            # If you are renaming the network, check if the network
            # already exists.
            new_dir = os.path.join(start_path,path)
            # If the network exists already raise a ValueError
            if os.path.isdir(new_dir):
                raise ValueError(f"Invalid new network directory <{new_dir}>")
            # Otherwise rename the directory.
            else:
                os.rename(self._path,new_dir)


    def add_router(self,router):
        self.routers.append(router)
