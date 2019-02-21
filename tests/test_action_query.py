from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from generic_query import SQLQueryAction

import mock

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

    @mock.patch('lib.base_action.BaseAction.db_connection')
    def test_run(self, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'query': 'generic query'
        }
        test_dict.update(connection_config)
        test_row = mock.Mock(test1='value', test2='value2')
        test_row.keys.return_value = ['test1', 'test2']
        expected_result = [{
            'test1': 'value',
            'test2': 'value2'
        }]
        mock_query_results = mock.Mock(returns_rows=True, rowcount=1)
        mock_query_results.fetchall.return_value = [test_row]
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = mock_query_results
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_connection.execute.assert_called_once_with(test_dict['query'])

    @mock.patch('lib.base_action.BaseAction.db_connection')
    def test_run_connction(self, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        test_dict = {
            'connection': connection_name,
            'query': 'generic query'
        }
        expected_result = {'affected_rows': 5}
        mock_query_results = mock.Mock(returns_rows=False, rowcount=5)
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = mock_query_results
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_connection.execute.assert_called_once_with(test_dict['query'])
