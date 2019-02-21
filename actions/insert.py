from lib.base_action import BaseAction
import sqlalchemy


class SQLInsertAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLInsertAction, self).__init__(config)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        insert_data = self.get_del_arg('data', kwargs_dict)
        insert_table = self.get_del_arg('table', kwargs_dict)

        if not isinstance(insert_data, list):
            insert_data = [insert_data]

        with self.db_connection(kwargs_dict) as conn:
            # Get the Table to insert data into
            sql_table = sqlalchemy.Table(insert_table,
                                        self.meta,
                                        autoload=True,
                                        autoload_with=self.engine)

            # Execute the insert query
            conn.execute(sql_table.insert(),  # pylint: disable-msg=no-value-for-parameter
                        insert_data)

        return True
