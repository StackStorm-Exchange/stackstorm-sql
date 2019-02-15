from lib.base_action import BaseAction


class SQLQueryAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLQueryAction, self).__init__(config)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        query = self.get_del_arg('query', kwargs_dict, True)

        # Get the connection details from either config or from action params
        connection_details = self.resolve_connection(kwargs_dict)

        # Connect to the Database
        self.connect_to_db(connection_details)

        # Execute the query
        query_result = self.conn.execute(query)

        return_result = {'affected_rows': query_result.rowcount}
        if query_result.returns_rows:
            return_result = []
            for row in query_result:
                # Rows are returned as tuples with keys. Convert that to a dictionary for return
                return_result.append(self.row_to_dict(row))

        # Disconnect from the database
        self.conn.close()

        return return_result
