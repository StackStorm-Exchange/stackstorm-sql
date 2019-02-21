from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from delete import SQLDeleteAction

import mock

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

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('delete.sqlalchemy')
    def test_run_object(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'table': 'Test_Table',
            'where': {
                'column_1': 'value_1'
            }
        }
        test_dict.update(connection_config)
        execute_dict = {'_column_1': 'value_1'}
        expected_result = {'affected_rows': 1}
        action_meta = 'MetaData'
        action_engine = "Engine Data"
        mock_where_return = "Where statment"
        mock_where = mock.Mock()
        mock_where.where.return_value = mock_where_return
        mock_sql_table = mock.Mock()
        mock_sql_table.delete.return_value = mock_where
        mock_query_results = mock.Mock(rowcount=1)
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = mock_query_results
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection
        action.meta = action_meta
        action.engine = action_engine
        mock_sqlalchemy.Table.return_value = mock_sql_table

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_sqlalchemy.Table.assert_called_once_with(test_dict['table'],
                                                      action_meta,
                                                      autoload=True,
                                                      autoload_with=action_engine)
        mock_connection.execute.assert_called_once_with(mock_where_return, execute_dict)

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('delete.sqlalchemy')
    def test_run_array(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        test_dict = {
            'connection': connection_name,
            'table': 'Test_Table'
        }
        expected_result = {'affected_rows': 20}
        action_meta = 'MetaData'
        action_engine = "Engine Data"
        mock_delete_return = "Delete Statement"
        mock_sql_table = mock.Mock()
        mock_sql_table.delete.return_value = mock_delete_return
        mock_query_results = mock.Mock(rowcount=20)
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = mock_query_results
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection
        action.meta = action_meta
        action.engine = action_engine
        mock_sqlalchemy.Table.return_value = mock_sql_table

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_sqlalchemy.Table.assert_called_once_with(test_dict['table'],
                                                      action_meta,
                                                      autoload=True,
                                                      autoload_with=action_engine)
        mock_connection.execute.assert_called_once_with(mock_delete_return, None)
