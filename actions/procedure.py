from lib.base_action import BaseAction
import sqlalchemy
from sqlalchemy.orm import sessionmaker


class SQLProcedureAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLProcedureAction, self).__init__(config)

    def format_data(self, proc_data_obj):
        proc_data_string = ""
        if proc_data_obj:
            proc_data_list = []
            for name, value in proc_data_obj.items():
                proc_data_list.append("@{0}='{1}'".format(name, value))

            proc_data_string = ",".join(proc_data_list)

        return proc_data_string

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        proc_data = self.get_del_arg('procedure_data', kwargs_dict)
        proc_data_string = self.format_data(proc_data)

        proc_name = self.get_del_arg('procedure_name', kwargs_dict)

        exec_stmt = "EXEC {} {}".format(proc_name, proc_data_string)

        database_connection_string = self.build_connection(kwargs_dict)
        engine = sqlalchemy.create_engine(database_connection_string)
        session = sessionmaker(bind=engine)()

        return_result = None
        try:
            exec_result = session.execute(exec_stmt)
            return_result = {'affected_rows': exec_result.rowcount}
            session.commit()
        except Exception as error:
            session.rollback()

            # Return error to the user
            raise error
        finally:
            session.close()

        return return_result
