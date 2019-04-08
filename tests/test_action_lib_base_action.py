from sql_base_action_test_case import SqlBaseActionTestCase

from lib.base_action import BaseAction
from lib.base_action import CONFIG_CONNECTION_KEYS
from st2common.runners.base_action import Action
from insert import SQLInsertAction
import decimal
import datetime

import copy
import mock

__all__ = [
    'TestActionLibBaseAction'
]


class TestActionLibBaseAction(SqlBaseActionTestCase):
    __test__ = True
    action_cls = SQLInsertAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    def test_get_del_arg_present(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key1"
        expected_dict = {"key2": "value2"}
        expected_value = test_dict["key1"]
        result_value = action.get_del_arg(test_key, test_dict, True)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)

    def test_get_del_arg_missing(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key3"
        expected_dict = test_dict
        expected_value = None
        result_value = action.get_del_arg(test_key, test_dict)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)

    def test_merge_dicts(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": [{"key1": "value1",
                                  "key2": "value2"},
                                 {"key3": "value3"}]}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {"key1": "value1",
                                  "key2": "value2",
                                  "key3": "value3"})

    def test_merge_dicts_overwrite(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": [{"key1": "value1",
                                  "key2": "value2"},
                                 {"key2": "overwrite value2"}]}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {"key1": "value1",
                                  "key2": "overwrite value2"})

    def test_merge_dicts_dict_none(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": [{"key1": "value1",
                                  "key2": "value2"},
                                 None]}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {"key1": "value1",
                                  "key2": "value2"})

    def test_merge_dicts_single(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": [{"key1": "value1",
                                  "key2": "value2"}]}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {"key1": "value1",
                                  "key2": "value2"})

    def test_merge_dicts_empty(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": []}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {})

    def test_merge_dicts_single_none(self):
        action = self.get_action_instance({})
        kwargs_dict = {"dicts": [None]}
        result = action.merge_dicts(**kwargs_dict)
        self.assertEqual(result, {})

    def test_row_to_dict(self):
        action = self.get_action_instance({})
        test_row = mock.Mock(test1='value', test2='value2')
        test_row.keys.return_value = ['test1', 'test2']
        expected_result = {
            'test1': 'value',
            'test2': 'value2'
        }
        result = action.row_to_dict(test_row)
        self.assertEqual(result, expected_result)

    def test_row_to_dict_unit_convert(self):
        action = self.get_action_instance({})
        test_row = mock.Mock(teststring='value',
                            testinteger=1,
                            testdecimal=decimal.Decimal('5.543'),
                            testfloat=2.352,
                            testdict={'test': 'value'},
                            testdatetime=datetime.datetime(2019, 1, 1, 0, 0))
        test_row.keys.return_value = ['teststring',
                                    'testinteger',
                                    'testdecimal',
                                    'testfloat',
                                    'testdict',
                                    'testdatetime']
        expected_result = {
            'testinteger': 1,
            'testdict': {'test': 'value'},
            'testdecimal': 5.543,
            'teststring': 'value',
            'testdatetime': '2019-01-01T00:00:00',
            'testfloat': 2.352
        }
        result = action.row_to_dict(test_row)
        self.assertEqual(result, expected_result)

    def test_generate_where_clause(self):
        action = self.get_action_instance({})
        test_dict = {
            'test_column': 'test_value'
        }
        expected_dict = {
            '_test_column': 'test_value'
        }
        expected_output = "Successfull Where Clause"
        mock_sql_obj = mock.Mock()
        mock_sql_obj.where.return_value = expected_output
        mock_sql_table_get = mock.Mock()
        mock_sql_table_get.get.return_value = 'Success'
        mock_sql_table = mock.Mock(c=mock_sql_table_get)

        result_obj, result_dict = action.generate_where_clause(mock_sql_table,
                                                               mock_sql_obj,
                                                               test_dict)
        self.assertEqual(result_obj, expected_output)
        self.assertEqual(result_dict, expected_dict)

    def test_generate_where_clause_multiple(self):
        action = self.get_action_instance({})
        test_dict = {
            'test_column': 'test_value',
            'test_column2': 'test_value2'
        }
        expected_dict = {
            '_test_column': 'test_value',
            '_test_column2': 'test_value2'
        }
        expected_output = "Successfull Where Clause"
        mock_sql_obj = mock.Mock()
        mock_sql_obj.where.side_effect = [mock_sql_obj, expected_output]
        mock_sql_table_get = mock.Mock()
        mock_sql_table_get.get.return_value = 'Success'
        mock_sql_table = mock.Mock(c=mock_sql_table_get)

        result_obj, result_dict = action.generate_where_clause(mock_sql_table,
                                                               mock_sql_obj,
                                                               test_dict)
        self.assertEqual(result_obj, expected_output)
        self.assertEqual(result_dict, expected_dict)

    def test_generate_values(self):
        action = self.get_action_instance({})
        test_dict = {
            'test_column': 'test_value'
        }
        expected_output = "Successfull"
        mock_sql_obj = mock.Mock()
        mock_sql_obj.values.return_value = expected_output

        result = action.generate_values(mock_sql_obj, test_dict)
        self.assertEqual(result, expected_output)

    def test_generate_values_multiple(self):
        action = self.get_action_instance({})
        test_dict = {
            'test_column': 'test_value',
            'test_column2': 'test_value2'
        }
        expected_output = "Successfull number 2"
        mock_sql_obj = mock.Mock()
        mock_sql_obj.values.side_effect = [mock_sql_obj, expected_output]

        result = action.generate_values(mock_sql_obj, test_dict)
        self.assertEqual(result, expected_output)

    @mock.patch('lib.base_action.sqlalchemy')
    def test_connect_to_db(self, mock_sqlalchemy):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        mock_engine = mock.Mock()
        mock_engine.connect.return_value = 'Connected'
        mock_sqlalchemy.create_engine.return_value = mock_engine
        mock_sqlalchemy.MetaData.return_value = 'MetaData'

        action.db_connection(connection_config)

    @mock.patch('lib.base_action.sqlalchemy')
    def test_connect_to_db_sqlite(self, mock_sqlalchemy):
        action = self.get_action_instance(self.config_good)
        connection_name = 'sqlite'
        connection_config = self.config_good['connections'][connection_name]
        mock_engine = mock.Mock()
        mock_engine.connect.return_value = 'Connected'
        mock_sqlalchemy.create_engine.return_value = mock_engine
        mock_sqlalchemy.MetaData.return_value = 'MetaData'

        action.db_connection(connection_config)

    def test_resolve_connection_from_config(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'full'
        connection_config = self.config_good['connections'][connection_name]
        connection_expected = {}
        connection_expected.update(connection_config)
        kwargs_dict = {'connection': connection_name}
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)

    def test_resolve_connection_from_config_missing(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'this_connection_doesnt_exist'
        kwargs_dict = {'connection': connection_name}
        with self.assertRaises(KeyError):
            action.resolve_connection(kwargs_dict)

    def test_resolve_connection_from_config_defaults(self):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['connections'][connection_name]
        connection_expected = {}
        connection_expected.update(connection_config)
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if not required and default:
                connection_expected[key] = default

        kwargs_dict = {'connection': connection_name}
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)

    def test_resolve_connection_from_kwargs(self):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'connection': None,
                       'host': 'kwargs_server',
                       'username': 'kwargs_username',
                       'password': 'kwargs_password',
                       'port': 123,
                       'database': 'abc123',
                       'drivername': 'postgresql'}
        connection_expected = copy.deepcopy(kwargs_dict)
        del connection_expected['connection']
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, {})

    def test_resolve_connection_from_kwargs_defaults(self):
        action = self.get_action_instance(self.config_blank)
        kwargs_dict = {'connection': None,
                       'database': 'test',
                       'drivername': 'postgresql'}
        connection_expected = copy.deepcopy(kwargs_dict)
        del connection_expected['connection']
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if not required and default:
                connection_expected[key] = default

        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, {})

    def test_resolve_connection_from_kwargs_extras(self):
        action = self.get_action_instance(self.config_blank)
        connection_expected = {'connection': None,
                               'host': 'kwargs_server',
                               'username': 'kwargs_username',
                               'password': 'kwargs_password',
                               'port': 123,
                               'database': 'abc123',
                               'drivername': 'postgresql'}
        kwargs_dict = copy.deepcopy(connection_expected)
        del connection_expected['connection']
        kwargs_extras = {"extra_key1": "extra_value1",
                         "extra_key2": 234}
        kwargs_dict.update(kwargs_extras)
        connection_result = action.resolve_connection(kwargs_dict)
        self.assertEqual(connection_result, connection_expected)
        self.assertEqual(kwargs_dict, kwargs_extras)

    def test_validate_connection(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if required:
                connection[key] = "value_for_key_{}".format(key)

        result = action.validate_connection(connection, True)
        self.assertTrue(result)

    def test_validate_connection_missing_raises(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        with self.assertRaises(KeyError):
            action.validate_connection(connection, True)

    def test_validate_connection_none_raises(self):
        action = self.get_action_instance(self.config_blank)
        connection = {}
        for key, required, default in CONFIG_CONNECTION_KEYS:
            connection[key] = None

        with self.assertRaises(KeyError):
            action.validate_connection(connection, False)
