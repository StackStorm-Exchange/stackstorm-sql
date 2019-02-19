from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from insert import SQLInsertAction

# import mock

__all__ = [
    'TestActionSQLInsertAction'
]


class TestActionSQLInsertAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLInsertAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SQLInsertAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)
