from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from update import SQLUpdateAction

# import mock

__all__ = [
    'TestActionSQLUpdateAction'
]


class TestActionSQLUpdateAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLUpdateAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SQLUpdateAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)
