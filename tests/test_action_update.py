from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from update import SQLUpdateAction

import mock

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

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('update.sqlalchemy')
    def test_run_object(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'table': 'Test_Table',
            'where': {
                'column_1': 'value_1'
            },
            'update': {
                'column_2': 'value_2'
            }
        }
        test_dict.update(connection_config)
        execute_dict = {'_column_1': 'value_1', 'column_2': 'value_2'}
        expected_result = {'affected_rows': 1}
        action_meta = 'MetaData'
        action_engine = "Engine Data"
        mock_values = mock.Mock()
        mock_values_return = "Where and Values object"
        mock_values.values.return_value = mock_values_return
        mock_where = mock.Mock()
        mock_where.where.return_value = mock_values
        mock_sql_table = mock.Mock()
        mock_sql_table.update.return_value = mock_where
        mock_sql_table.c.get.return_value = "column return"
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
        mock_connection.execute.assert_called_once_with(mock_values_return, execute_dict)

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('update.sqlalchemy')
    def test_run_array(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        test_dict = {
            'connection': connection_name,
            'table': 'Test_Table',
            'update': {
                'column_2': 'value_2'
            }
        }
        expected_result = {'affected_rows': 20}
        action_meta = 'MetaData'
        action_engine = "Engine Data"
        mock_values = mock.Mock()
        mock_values_return = "Where and Values object"
        mock_values.values.return_value = mock_values_return
        mock_sql_table = mock.Mock()
        mock_sql_table.update.return_value = mock_values
        mock_sql_table.c.get.return_value = "column return"
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
        mock_connection.execute.assert_called_once_with(mock_values_return,
                                                        test_dict['update'])
