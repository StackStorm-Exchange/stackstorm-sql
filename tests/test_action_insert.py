from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from insert import SQLInsertAction

import mock

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

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('insert.sqlalchemy')
    def test_run_object(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'table': 'Test_Table',
            'data': {
                'column_1': 'value_1',
                'column_2': 'value_2'
            }
        }
        test_dict.update(connection_config)
        action_meta = "MetaData"
        action_engine = "Engine Data"
        mock_sql_table = mock.Mock()
        insert_return = "Insert Statment"
        mock_sql_table.insert.return_value = insert_return
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = "Successfully Executed Statement"
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection
        action.meta = action_meta
        action.engine = action_engine
        mock_sqlalchemy.Table.return_value = mock_sql_table

        result = action.run(**test_dict)
        self.assertEqual(result, True)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_sqlalchemy.Table.assert_called_once_with(test_dict['table'],
                                                      action_meta,
                                                      autoload=True,
                                                      autoload_with=action_engine)
        mock_connection.execute.assert_called_once_with(insert_return, [test_dict['data']])

    @mock.patch('lib.base_action.BaseAction.db_connection')
    @mock.patch('insert.sqlalchemy')
    def test_run_array(self, mock_sqlalchemy, mock_connect_to_db):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        test_dict = {
            'connection': connection_name,
            'table': 'Test_Table',
            'data': [{
                'column_1': 'value_1',
                'column_2': 'value_2'
            }, {
                'column_1': 'value_3',
                'column_2': 'value_4'
            }]
        }
        action_meta = "MetaData"
        action_engine = "Engine Data"
        mock_sql_table = mock.Mock()
        insert_return = "Insert Statment"
        mock_sql_table.insert.return_value = insert_return
        mock_connection = mock.Mock()
        mock_connection.execute.return_value = "Successfully Executed Statement"
        mock_connection.close.return_value = "Successfully disconnected"
        mock_connect_to_db.return_value.__enter__.return_value = mock_connection

        action.conn = mock_connection
        action.meta = action_meta
        action.engine = action_engine
        mock_sqlalchemy.Table.return_value = mock_sql_table

        result = action.run(**test_dict)
        self.assertEqual(result, True)
        mock_connect_to_db.assert_called_once_with(test_dict)
        mock_sqlalchemy.Table.assert_called_once_with(test_dict['table'],
                                                      action_meta,
                                                      autoload=True,
                                                      autoload_with=action_engine)
        mock_connection.execute.assert_called_once_with(insert_return, test_dict['data'])
