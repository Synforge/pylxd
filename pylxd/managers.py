from contextlib import contextmanager

import functools
import importlib
import inspect


class BaseManager(object):
    """A BaseManager class for handling collection operations."""

    @property
    def manager_for(self):  # pragma: no cover
        raise AttributeError(
            "Manager class requires 'manager_for' attribute")

    def __init__(self, *args, **kwargs):
        manager_for = self.manager_for
        module = '.'.join(manager_for.split('.')[0:-1])
        obj = manager_for.split('.')[-1]
        target_module = importlib.import_module(module)
        target = getattr(target_module, obj)

        methods = inspect.getmembers(target, predicate=inspect.ismethod)
        for name, method in methods:
            func = functools.partial(method, *args, **kwargs)
            setattr(self, name, func)
        return super(BaseManager, self).__init__()


class CertificateManager(BaseManager):
    manager_for = 'pylxd.models.Certificate'


class ContainerManager(BaseManager):
    manager_for = 'pylxd.models.Container'


class ImageManager(BaseManager):
    manager_for = 'pylxd.models.Image'


class NetworkManager(BaseManager):
    manager_for = 'pylxd.models.Network'


class OperationManager(BaseManager):
    manager_for = 'pylxd.models.Operation'


class ProfileManager(BaseManager):
    manager_for = 'pylxd.models.Profile'


class SnapshotManager(BaseManager):
    manager_for = 'pylxd.models.Snapshot'


@contextmanager
def web_socket_manager(manager):
    try:
        yield manager
    finally:
        manager.stop()
