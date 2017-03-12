#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Stub out a basic exceptions, mostly used by objects."""


class KwException(Exception):
    def __init__(self, *args, **kwargs):
        kwargs = kwargs or {}
        super(KwException, self).__init__(
            '%s: %s' % (self.__class__.__name__, str(kwargs)))


class NotFound(KwException):
    pass


class ResourceProviderInUse(Exception):
    pass


class ResourceClassExists(KwException):
    pass


class ResourceClassNotFound(NotFound):
    pass


class ResourceClassCannotDeleteStandard(KwException):
    pass


class ConcurrentUpdateDetected(Exception):
    pass


class MaxDBRetriesExceeded(KwException):
    pass


class InvalidInventory(Exception):
    pass

class InventoryWithResourceClassNotFound(KwException):
    pass


class InventoryInUse(Exception):
    pass


class InvalidInventoryCapacity(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidInventoryCapacity, self).__init__(
            'invalid inv cap: %s' % str(kwargs))


class ObjectActionError(Exception):

    def __init__(self, *args, **kwargs):
        super(ObjectActionError, self).__init__(
            'object action error: %s' % str(kwargs))
