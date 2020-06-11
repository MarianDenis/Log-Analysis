import os
from time import time

from pkg_clustering import dbscan as db
from pkg_elastic import fields as fd
from pkg_elastic import connection as con


def get_clusters(date_time, number_of_logs):
    print('Attempting hierarchical clusterization...*')
    start_time = time()
    one_el_cluster_array = []
    connection = con.Connection(date_time, number_of_logs)
    logs = connection.get_logs_sql_inj()  # array de dictionare
    # i_gen.append_logs(logs)
    current_directory = os.path.dirname(os.getcwd())

    print('Methods level...*')
    met_clusters = db.run_dbscan(logs, 0.2, 2, fd.Fields.Method)
    met_dict = db.get_clusters_dictionary(met_clusters, logs)

    file = current_directory + '\\Clusters\\1_methods.txt'
    met_file = open(file, 'w+')
    for x in met_dict:
        met_file.write('\nCluster ' + str(x) + ':\n')
        for y in met_dict[x]:
            met_file.write(str(y) + '\n')
    met_file.close()

    print('Request level...*')
    req_array = []
    for log in met_dict.values():
        if len(log) > 1:
            request_clusters = db.run_dbscan(log, 0.5, 10, fd.Fields.Request)
            req_dict = db.get_clusters_dictionary(request_clusters, log)

            req_array.append(req_dict)
        else:
            one_el_cluster_array.append(log)

    file = current_directory + '\\Clusters\\2_requests.txt'
    req_file = open(file, 'w+')
    for idx, val in enumerate(req_array):
        # req_file.write('\nMethod ' + str(idx) + ':\n')
        for y in val:
            req_file.write('\nCluster ' + str(y) + ':\n')
            for z in val[y]:
                req_file.write(str(z) + '\n')
        req_file.write('\n -------------------------------------------------- \n')
    req_file.close()

    print('Response class level...*')
    resp_class_array = []
    for log in req_array:
        for sublog in log.values():
            if len(sublog) > 1:
                resp_class_clusters = db.run_dbscan(sublog, 100, 5, fd.Fields.Resp_Class)
                resp_cl_dict = db.get_clusters_dictionary(resp_class_clusters, sublog)

                resp_class_array.append(resp_cl_dict)
            else:
                one_el_cluster_array.append(sublog)

    file = current_directory + '\\Clusters\\3_respClass.txt'
    resp_class_file = open(file, 'w+')
    for idx, val in enumerate(resp_class_array):
        # resp_class_file.write('\nRequest ' + str(idx) + ':\n')
        for y in val:
            resp_class_file.write('\nCluster ' + str(y) + ':\n')
            for z in val[y]:
                resp_class_file.write(str(z) + '\n')
        resp_class_file.write('\n -------------------------------------------------- \n')
    resp_class_file.close()

    print('Response code level...*')
    resp_code_array = []
    for log in resp_class_array:
        for sublog in log.values():
            if len(sublog) > 1:
                resp_code_clusters = db.run_dbscan(sublog, 1, 10, fd.Fields.Resp_Code)
                resp_code_dict = db.get_clusters_dictionary(resp_code_clusters, sublog)

                resp_code_array.append(resp_code_dict)
            else:
                one_el_cluster_array.append(sublog)

    file = current_directory + '\\Clusters\\4_responseCode.txt'
    resp_code_file = open(file, 'w+')
    for idx, val in enumerate(resp_code_array):
        # resp_code_file.write('\nResponse Class ' + str(idx) + ':\n')
        for y in val:
            resp_code_file.write('\nCluster ' + str(y) + ':\n')
            for z in val[y]:
                resp_code_file.write(str(z) + '\n')
        resp_code_file.write('\n -------------------------------------------------- \n')
    resp_code_file.close()

    print('Data trasfered level...*')
    data_tranf_array = []
    for log in resp_code_array:
        for sublog in log.values():
            if len(sublog) > 1:
                data_transf_clusters = db.run_dbscan(sublog, 2000, 5, fd.Fields.Data_Transf)
                data_transf_dict = db.get_clusters_dictionary(data_transf_clusters, sublog)

                data_tranf_array.append(data_transf_dict)
            else:
                one_el_cluster_array.append(sublog)

    file = current_directory + '\\Clusters\\6_data_tranf.txt'
    data_transf_file = open(file, 'w+')
    for idx, val in enumerate(data_tranf_array):
        # data_transf_file.write('\nQuery' + str(idx) + ':\n')
        for y in val:
            data_transf_file.write('\nCluster ' + str(y) + ':\n')
            for z in val[y]:
                data_transf_file.write(str(z) + '\n')
        data_transf_file.write('\n -------------------------------------------------- \n')
    data_transf_file.close()

    print('Query level...*')
    query_array = []
    for log in data_tranf_array:
        for sublog in log.values():
            if len(sublog) > 1:
                query_cluster = db.run_dbscan(sublog, 0.4, 10, fd.Fields.Query)
                querry_dict = db.get_clusters_dictionary(query_cluster, sublog)

                query_array.append(querry_dict)
            else:
                one_el_cluster_array.append(sublog)

    file = current_directory + '\\Clusters\\5_query.txt'
    query_file = open(file, 'w+')
    for idx, val in enumerate(query_array):
        # query_file.write('\nResponse Code ' + str(idx) + ':\n')
        for y in val:
            query_file.write('\nCluster ' + str(y) + ':\n')
            for z in val[y]:
                query_file.write(str(z) + '\n')
        query_file.write('\n -------------------------------------------------- \n')
    query_file.close()

    file = current_directory + '\\Clusters\\8_oec.txt'
    one_el_cluster_file = open(file, 'w+')
    for x in one_el_cluster_array:
        one_el_cluster_file.write('\n' + str(x))

    one_el_cluster_file.close()
    print(f'Clusterization completed -> {time() - start_time}')

    return one_el_cluster_array, query_array, met_dict, req_array, resp_class_array, resp_code_array, data_tranf_array
