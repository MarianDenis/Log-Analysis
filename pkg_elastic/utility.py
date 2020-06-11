import elasticsearch as elk
from pkg_utility import date_conversion as dc


def get_connection(index_name: str):
    es = elk.Elasticsearch()
    index = index_name

    try:
        elastic = elk.Elasticsearch(
            ["localhost:9200"],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60
        )
    except Exception as error:
        print("Elasticsearch Client Error:", error)
        # make a default connection if error
        elastic = elk.Elasticsearch()
    return es, index


# def get_logs(startdate: str):
#     es, index = get_connection("index_three")
#     # query = get_query()
#     query = get_query_for_day(startdate)
#     logs = es.search(index=index, body=query)
#
#     hits_overall = logs['hits']
#     hits = hits_overall['hits']
#     for log in hits:
#         source = log['_source']
#         if source['referer'] != '-':
#             yield [source['referer'], source['request']]


def get_logs_for_cluster(startdate: str, number_of_logs):
    es, index = get_connection("index_three")
    query = get_query_for_day(startdate, number_of_logs)
    logs = es.search(index=index, body=query)

    hits_overall = logs['hits']
    hits = hits_overall['hits']
    result = []
    for log in hits:
        source = log['_source']
        dictionar = {}

        if 'client_ip' in source:
            dictionar['client_ip'] = source['client_ip']
        if 'method' in source:
            dictionar['method'] = source['method']
        if 'request' in source:
            dictionar['request'] = source['request']
        if 'response_code_class' in source:
            dictionar['response_code_class'] = source['response_code_class']
        if 'response_code' in source:
            dictionar['response_code'] = source['response_code']
        if 'query' in source:
            dictionar['query'] = source['query']
        if 'data_transfered' in source:
            dictionar['data_transfered'] = source['data_transfered']

        result.append(dictionar)
    return result


num_of_logs_for_sql_injection = 500
num_of_logs_for_dos = 10000


def get_query_for_day(start_date: str, num_of_logs):  # start_date: dt.datetime
    current_date, time_zone = dc.get_date_from_elk_date_format(start_date)
    current_date = dc.get_date_after(current_date, 1)
    end_date = dc.get_elk_date_format_from_date(current_date, time_zone)  # calculeaza data dupa o zi


    query = """
    {
      "version": true,
      "size": """ + str(num_of_logs) + """,
      "sort": [
        {
          "@timestamp": {
            "order": "asc",
            "unmapped_type": "boolean"
          }
        }
      ],
      "aggs": {
        "2": {
          "date_histogram": {
            "field": "@timestamp",
            "fixed_interval": "30m",
            "time_zone": "Europe/Bucharest",
            "min_doc_count": 1
          }
        }
      },
      "stored_fields": [
        "*"
      ],
      "script_fields": {},
      "docvalue_fields": [
        {
          "field": "@timestamp",
          "format": "date_time"
        }
      ],
      "_source": {
        "includes": ["client_ip", "method", "request", "response_code_class", "response_code", "query", "data_transfered"],
        "excludes": []
      },
      "query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "match_all": {}
            },
            {
              "range": {
                "@timestamp": {
                  "gte": """ + '"' + start_date + '"' + """,
                  "lte": """ + '"' + end_date + '"' + """,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      },
      "highlight": {
        "pre_tags": [
          "@kibana-highlighted-field@"
        ],
        "post_tags": [
          "@/kibana-highlighted-field@"
        ],
        "fields": {
          "*": {}
        },
        "fragment_size": 2147483647
      }
    }
    """

    return query


# def get_logs_for_dos(start_date: str):
#     es, index = get_connection("last_index")
#     query = get_dos_query_for_day(start_date)
#     logs = es.search(index=index, body=query)
#
#     hits_overall = logs['hits']
#     hits = hits_overall['hits']
#     for log in hits:
#         source = log['_source']
#         if source['referer'] != '-':
#             yield [source['referer'], source['request']]


def get_logs_for_dos_final(start_date: str):
    es, index = get_connection("last_index")
    query = get_dos_query_for_day(start_date)
    logs = es.search(index=index, body=query)

    hits_overall = logs['hits']
    hits = hits_overall['hits']
    for log in hits:
        source = log['_source']
        if source['referer'] != '-':
            yield [source['client_ip'], source['referer'], source['request']]


def get_dos_query_for_day(start_date: str):
    current_date, time_zone = dc.get_date_from_elk_date_format(start_date)
    current_date = dc.get_date_after(current_date, 1)
    end_date = dc.get_elk_date_format_from_date(current_date, time_zone)  # calculeaza data dupa o zi

    query = """
    {
      "version": true,
      "size": """ + str(num_of_logs_for_dos) + """,
      "sort": [
        {
          "@timestamp": {
            "order": "desc",
            "unmapped_type": "boolean"
          }
        }
      ],
      "aggs": {
        "2": {
          "date_histogram": {
            "field": "@timestamp",
            "fixed_interval": "30m",
            "time_zone": "Europe/Bucharest",
            "min_doc_count": 1
          }
        }
      },
      "stored_fields": [
        "*"
      ],
      "script_fields": {},
      "docvalue_fields": [
        {
          "field": "@timestamp",
          "format": "date_time"
        }
      ],
      "_source": {
        "excludes": []
      },
      "query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "match_all": {}
            },
            {
              "range": {
                "@timestamp": {
                  "gte": """ + '"' + start_date + '"' + """,
                  "lte": """ + '"' + end_date + '"' + """,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      },
      "highlight": {
        "pre_tags": [
          "@kibana-highlighted-field@"
        ],
        "post_tags": [
          "@/kibana-highlighted-field@"
        ],
        "fields": {
          "*": {}
        },
        "fragment_size": 2147483647
      }
    }
    """

    return query
