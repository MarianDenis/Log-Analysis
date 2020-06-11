import os
import re

from pkg_clustering import hierarchical_clustering as hc
from pkg_injection import blacklist as bl


def inspect_noise_logs(resulted_logs):
    noise_logs = []

    current_directory = os.path.dirname(os.getcwd())
    file = current_directory + '\\Clusters\\NoiseClusters.txt'
    noise_logs_file = open(file, 'w+')
    for idx, val in enumerate(resulted_logs):
        for cluster in val:
            if cluster == -1:
                noise_logs_file.write('\n --------- \n')
                for log in val[cluster]:
                    if 'query' in log:
                        noise_logs_file.write(str(log) + '\n')
                        noise_logs.append(log)
    return noise_logs


def test_logs(date_time, number_of_logs):
    one_el_cluster_logs, resulted_logs, met_a, req_a, rclass_a, rcode_a, dt_a = hc.get_clusters(date_time,
                                                                                                number_of_logs)

    print("Searching for instrusions...*")
    noise_logs = inspect_noise_logs(resulted_logs)
    logs = []
    for idx, log in enumerate(noise_logs):
        if check_query(log):
            logs.append(log)

    for log in one_el_cluster_logs:
        if 'query' in log[0]:
            if check_query(log[0]):
                logs.append(log[0])

    for idx, val in enumerate(resulted_logs):
        for cluster in val:
            if cluster != -1:
                log = val[cluster][0]
                if 'query' in log:
                    if check_query(log):
                        for lg in val[cluster]:
                            logs.append(lg)
    print("Intrusion search completed!")
    return resulted_logs, logs, met_a, req_a, rclass_a, rcode_a, dt_a


def check_query(log):
    # sql_keywords = sqlK.get_keywords()

    split_query_pattern = "(?:(?=&)(?!(?:&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;))&)"
    query = log['query']

    if bl.SqlKewords.Truism.value[0] in query:
        return True

    tokens = []
    for token in re.split(split_query_pattern, query):
        try:
            token = token.split("=", 1)[1]
            tokens.append(token)
        except IndexError:
            pass
    return check_for_intrusion(tokens)


def check_for_intrusion(tokens: []):
    for token in tokens:
        if check_for_sql_injection(token):
            return True
        elif check_for_xss(token):
            return True
        elif check_for_command_injection(token):
            return True
    return False


def check_for_sql_injection(token):
    sql_keywords = bl.get_keywords()
    sql_or_pattern = "((%27|'|&apos;).*%20|\\+| |&nbsp;)(or|and)(?:%20|\\+| |&nbsp;)"
    if any(keyword.casefold() in token.casefold() for keyword in sql_keywords):
        return True
    if re.search(sql_or_pattern, token, re.IGNORECASE):
        return True
    return False


def check_for_xss(token):
    xss_pattern = "(<|&lt;)/*[^<>]*(applet|meta|xml|blink|link|style|script|embed|object|iframe|frame" \
                  "|frameset|ilayer|layer|bgsound|title|base)[^>]*(>|&gt;)"
    xss_pattern_js = "((java|live|vb)script|mocha):(\w)*"
    if re.search(xss_pattern, token, re.IGNORECASE):
        return True
    elif re.search(xss_pattern_js, token, re.IGNORECASE):
        return True
    else:
        return False


def check_for_command_injection(token):
    com_inj_pattern = "(;|`|&|&&|\\||\\||).*(rm |cp |cat |ls |at |net |netstat |del |copy |etc(?:/| )|echo |dir )"
    if re.search(com_inj_pattern, token, re.IGNORECASE):
        return True
    else:
        return False


def write_bad_logs(logs):
    current_directory = os.path.dirname(os.getcwd())
    file = current_directory + '\\Intrusions\\SqlInjections.txt'
    intrusion_file = open(file, 'w+')
    for idx, log in enumerate(logs):
        intrusion_file.write(str(log) + "\n")
