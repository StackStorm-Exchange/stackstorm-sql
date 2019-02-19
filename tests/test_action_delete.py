from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from delete import SQLDeleteAction

# import mock

__all__ = [
    'TestActionSQLDeleteAction'
]


class TestActionSQLDeleteAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLDeleteAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SQLDeleteAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)
