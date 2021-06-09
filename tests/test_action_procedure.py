from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from st2common.runners.base_action import Action
from procedure import SQLProcedureAction
from sqlalchemy.engine.url import URL

import mock

__all__ = [
    'TestActionSQLProcedureAction'
]


class TestActionSQLProcedureAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLProcedureAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SQLProcedureAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    def test_format_data(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        expected_result = "@key1='value1',@key2='value2'"
        result = action.format_data(test_dict)
        self.assertEqual(result, expected_result)

    def test_format_data_none(self):
        action = self.get_action_instance({})
        test_dict = {}
        expected_result = ""
        result = action.format_data(test_dict)
        self.assertEqual(result, expected_result)

    @mock.patch('procedure.sessionmaker')
    @mock.patch('procedure.sqlalchemy')
    def test_run(self, mock_sqlalchemy, mock_sessionmaker):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'procedure_name': 'Test_Procedure',
            'procedure_data': {
                'column_1': 'value_1',
                'column_2': 'value_2'
            }
        }
        test_dict.update(connection_config)
        mock_sqlalchemy.create_engine.return_value = 'Mock Engine'
        mock_session = mock.Mock()
        mock_exec = mock.Mock(rowcount=1, returns_rows=False)
        mock_session().execute.return_value = mock_exec
        mock_sessionmaker.return_value = mock_session
        expected_value = {'affected_rows': 1}
        expected_call = "EXEC Test_Procedure @column_1='value_1',@column_2='value_2'"

        result = action.run(**test_dict)
        self.assertEqual(result, expected_value)
        mock_sqlalchemy.create_engine.assert_called_once_with(URL(**connection_config))
        mock_sessionmaker.assert_called_once_with(bind='Mock Engine')
        mock_session().execute.assert_called_once_with(expected_call)

    @mock.patch('procedure.sessionmaker')
    @mock.patch('procedure.sqlalchemy')
    def test_run_return_rows(self, mock_sqlalchemy, mock_sessionmaker):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        test_dict = {
            'procedure_name': 'Test_Procedure',
            'procedure_data': {
                'column_1': 'value_1',
                'column_2': 'value_2'
            }
        }
        test_dict.update(connection_config)
        mock_sqlalchemy.create_engine.return_value = 'Mock Engine'
        mock_session = mock.Mock()
        test_row = mock.Mock(test1='value', test2='value2')
        test_row.keys.return_value = ['test1', 'test2']
        mock_exec = mock.Mock(rowcount=-1, returns_rows=True)
        mock_exec.fetchall.return_value = [test_row]
        mock_session().execute.return_value = mock_exec
        mock_sessionmaker.return_value = mock_session
        expected_result = [{
            'test1': 'value',
            'test2': 'value2'
        }]
        expected_call = "EXEC Test_Procedure @column_1='value_1',@column_2='value_2'"

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_sqlalchemy.create_engine.assert_called_once_with(URL(**connection_config))
        mock_sessionmaker.assert_called_once_with(bind='Mock Engine')
        mock_session().execute.assert_called_once_with(expected_call)
