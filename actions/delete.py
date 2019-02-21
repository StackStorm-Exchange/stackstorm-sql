from lib.base_action import BaseAction
import sqlalchemy


class SQLDeleteAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLDeleteAction, self).__init__(config)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        where_dict = self.get_del_arg('where', kwargs_dict)
        table = self.get_del_arg('table', kwargs_dict)

        with self.db_connection(kwargs_dict) as conn:
            # Get the SQL table
            sql_table = sqlalchemy.Table(table,
                                        self.meta,
                                        autoload=True,
                                        autoload_with=self.engine)

            # Intantiate delete object
            delete = sql_table.delete()  # pylint: disable-msg=no-value-for-parameter

            # Generate Where Statement
            if where_dict:
                delete, where_dict = self.generate_where_clause(sql_table, delete, where_dict)

            # Execute query
            result = conn.execute(delete, where_dict)

        return {'affected_rows': result.rowcount}
