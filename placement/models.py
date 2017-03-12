#
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


from oslo_db.sqlalchemy import models
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy.orm import backref
from sqlalchemy import schema
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Unicode


class _PlacementBase(models.ModelBase, models.TimestampMixin):
    pass


BASE = declarative_base(cls=_PlacementBase)


class Allocation(BASE):
    """A use of inventory."""

    __tablename__ = "allocations"
    __table_args__ = (
        Index('allocations_resource_provider_class_used_idx',
              'resource_provider_id', 'resource_class_id',
              'used'),
        Index('allocations_resource_class_id_idx',
              'resource_class_id'),
        Index('allocations_consumer_id_idx', 'consumer_id')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    resource_provider_id = Column(Integer, nullable=False)
    consumer_id = Column(String(36), nullable=False)
    resource_class_id = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False)
    resource_provider = orm.relationship(
        "ResourceProvider",
        primaryjoin=('Allocation.resource_provider_id == '
                     'ResourceProvider.id'),
        foreign_keys=resource_provider_id)


class Inventory(BASE):
    """Represents a quantity of available resource."""

    __tablename__ = "inventories"
    __table_args__ = (
        Index('inventories_resource_provider_id_idx',
              'resource_provider_id'),
        Index('inventories_resource_class_id_idx',
              'resource_class_id'),
        Index('inventories_resource_provider_resource_class_idx',
              'resource_provider_id', 'resource_class_id'),
        schema.UniqueConstraint('resource_provider_id', 'resource_class_id',
            name='uniq_inventories0resource_provider_resource_class')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    resource_provider_id = Column(Integer, nullable=False)
    resource_class_id = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    reserved = Column(Integer, nullable=False)
    min_unit = Column(Integer, nullable=False)
    max_unit = Column(Integer, nullable=False)
    step_size = Column(Integer, nullable=False)
    allocation_ratio = Column(Float, nullable=False)
    resource_provider = orm.relationship(
        "ResourceProvider",
        primaryjoin=('Inventory.resource_provider_id == '
                     'ResourceProvider.id'),
        foreign_keys=resource_provider_id)


class PlacementAggregate(BASE):
    """A grouping of resource providers."""
    __tablename__ = 'placement_aggregates'
    __table_args__ = (
        schema.UniqueConstraint("uuid", name="uniq_placement_aggregates0uuid"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), index=True)


class ResourceClass(BASE):
    """Represents the type of resource for an inventory or allocation."""
    __tablename__ = 'resource_classes'
    __table_args__ = (
        schema.UniqueConstraint("name", name="uniq_resource_classes0name"),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)


class ResourceProvider(BASE):
    """Represents a mapping to a providers of resources."""

    __tablename__ = "resource_providers"
    __table_args__ = (
        Index('resource_providers_uuid_idx', 'uuid'),
        schema.UniqueConstraint('uuid',
            name='uniq_resource_providers0uuid'),
        Index('resource_providers_name_idx', 'name'),
        schema.UniqueConstraint('name',
            name='uniq_resource_providers0name')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(String(36), nullable=False)
    name = Column(Unicode(200), nullable=True)
    generation = Column(Integer, default=0)
    can_host = Column(Integer, default=0)


class ResourceProviderAggregate(BASE):
    """Associate a resource provider with an aggregate."""

    __tablename__ = 'resource_provider_aggregates'
    __table_args__ = (
        Index('resource_provider_aggregates_aggregate_id_idx',
              'aggregate_id'),
    )

    resource_provider_id = Column(Integer, primary_key=True, nullable=False)
    aggregate_id = Column(Integer, primary_key=True, nullable=False)
