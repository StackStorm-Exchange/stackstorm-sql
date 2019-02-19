from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from generic_query import SQLQueryAction

# import mock

__all__ = [
    'TestActionSQLQueryAction'
]


class TestActionSQLQueryAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLQueryAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SQLQueryAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)
