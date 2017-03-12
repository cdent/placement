# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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

import os

from migrate import exceptions as versioning_exceptions
from migrate.versioning import api as versioning_api
from migrate.versioning.repository import Repository
from oslo_db.sqlalchemy import utils as db_utils
from oslo_log import log as logging
import sqlalchemy
from sqlalchemy.sql import null

from placement import db as db_session
from placement import exception
from placement.i18n import _

INIT_VERSION = {}
INIT_VERSION['main'] = 0
_REPOSITORY = {}

LOG = logging.getLogger(__name__)


def get_engine(database='main', context=None):
    if database == 'main':
        return db_session.get_engine(context=context)


def db_sync(version=None, database='main', context=None):
    if version is not None:
        # Let ValueError raise
        version = int(version)

    current_version = db_version(database, context=context)
    repository = _find_migrate_repo(database)
    if version is None or version > current_version:
        return versioning_api.upgrade(get_engine(database, context=context),
                repository, version)
    else:
        return versioning_api.downgrade(get_engine(database, context=context),
                repository, version)


def db_version(database='main', context=None):
    repository = _find_migrate_repo(database)
    try:
        return versioning_api.db_version(get_engine(database, context=context),
                                         repository)
    except versioning_exceptions.DatabaseNotControlledError as exc:
        meta = sqlalchemy.MetaData()
        engine = get_engine(database, context=context)
        meta.reflect(bind=engine)
        tables = meta.tables
        if len(tables) == 0:
            db_version_control(INIT_VERSION[database],
                               database,
                               context=context)
            return versioning_api.db_version(
                        get_engine(database, context=context), repository)
        else:
            LOG.exception(exc)
            raise


def db_initial_version(database='main'):
    return INIT_VERSION[database]


def db_version_control(version=None, database='main', context=None):
    repository = _find_migrate_repo(database)
    versioning_api.version_control(get_engine(database, context=context),
                                   repository,
                                   version)
    return version


def _find_migrate_repo(database='main'):
    """Get the path for the migrate repository."""
    global _REPOSITORY
    rel_path = 'migrate_repo'
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        rel_path)
    assert os.path.exists(path)
    if _REPOSITORY.get(database) is None:
        _REPOSITORY[database] = Repository(path)
    return _REPOSITORY[database]
