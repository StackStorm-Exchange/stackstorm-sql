from lib.base_action import BaseAction
import sqlalchemy


class SQLUpdateAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLUpdateAction, self).__init__(config)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        where_dict = self.get_del_arg('where', kwargs_dict)
        update_dict = self.get_del_arg('update', kwargs_dict)
        table = self.get_del_arg('table', kwargs_dict)

        with self.db_connection(kwargs_dict) as conn:
            # Get the SQL table
            sql_table = sqlalchemy.Table(table,
                                        self.meta,
                                        autoload=True,
                                        autoload_with=self.engine)

            # Intantiate update object
            updates = sql_table.update()  # pylint: disable-msg=no-value-for-parameter

            # Generate Where Statement
            if where_dict:
                updates, where_dict = self.generate_where_clause(sql_table, updates, where_dict)

            updates = self.generate_values(updates, update_dict)

            # Combine Dictionaries
            query_dict = self.merge_dicts([where_dict, update_dict])

            # Execute query
            result = conn.execute(updates, query_dict)

        return {'affected_rows': result.rowcount}
