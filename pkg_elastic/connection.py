from pkg_elastic import utility as elk


# "2019-07-26T12:00:00.000Z"
# "2019-03-03T02:00:00.000Z"
def get_complete_logs_dos(start_date: str):
    return elk.get_logs_for_dos_final(start_date)


class Connection:

    def __init__(self, date_time, number_of_logs):
        #self.logs_sql_inj = elk.get_logs_for_cluster("2019-03-03T02:30:00.000Z")
        self.logs_sql_inj = elk.get_logs_for_cluster(date_time, number_of_logs)

    def get_logs_sql_inj(self):
        return self.logs_sql_inj
