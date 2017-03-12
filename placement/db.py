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

from oslo_db.sqlalchemy import enginefacade

# The maximum value a signed INT type may have
MAX_INT = 0x7FFFFFFF

# NOTE(dosaboy): This is supposed to represent the maximum value that we can
# place into a SQL single precision float so that we can check whether values
# are oversize. Postgres and MySQL both define this as their max whereas Sqlite
# uses dynamic typing so this would not apply. Different dbs react in different
# ways to oversize values e.g. postgres will raise an exception while mysql
# will round off the value. Nevertheless we may still want to know prior to
# insert whether the value is oversize or not.
SQL_SP_FLOAT_MAX = 3.40282e+38

main_context_manager = enginefacade.transaction_context()


def _context_manager_from_context(context):
    if context:
        try:
            return context.db_connection
        except AttributeError:
            pass


def get_context_manager(context):
    """Get a database context manager object.

    :param context: The request context that can contain a context manager
    """
    return _context_manager_from_context(context) or main_context_manager


def get_engine(use_slave=False, context=None):
    """Get a database engine object.

    :param use_slave: Whether to use the slave connection
    :param context: The request context that can contain a context manager
    """
    ctxt_mgr = get_context_manager(context)
    return ctxt_mgr.get_legacy_facade().get_engine(use_slave=use_slave)
