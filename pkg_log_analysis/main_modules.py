from pkg_injection import detection as det_inj
from pkg_plotting import plot_design as pd
from pkg_dos import apriori


def detect_sqli(r_date, r_time, number_of_logs):
    date_time = construct_datetime(r_date, r_time)
    resulted_logs, bad_logs, met_a, req_a, rclass_a, rcode_a, dt_a = det_inj.test_logs(date_time, number_of_logs)
    det_inj.write_bad_logs(bad_logs)

    return [[met_a], req_a, rclass_a, rcode_a, dt_a, resulted_logs]


def show_graph(clusters, graph_size):
    cplot = pd.ClusterPlot(clusters, graph_size)
    cplot.make_plot()


def construct_datetime(r_date, r_time):
    return r_date + "T" + r_time + ".000Z"


def detect_dos(r_date, r_time, num_of_days):
    ndays = int(num_of_days)
    date_time = construct_datetime(r_date, r_time)
    apriori.get_freq_items(date_time, ndays, 200)


if __name__ == '__main__':
    print(construct_datetime("2019-02-03", "02:03:03"))
