from _collections import defaultdict

from pkg_utility import date_conversion as du
from pkg_dos import utility as util
from pkg_elastic import connection as con


def get_items_and_transaction_list(records):
    transaction_list = list()  # lista cu tranzactii; ex: [{i1,i2}, {i3,i4,i5}]
    item_sets = set()  # ex: [{i1}, {i2}, {i3}]
    for record in records:  # fiecare linie din fisier reprezinta o tranzactie
        tran = frozenset(record)
        transaction_list.append(tran)
        for item in tran:  # preia toate item-ele din tranzactii, va rezulta L1
            item_sets.add(frozenset([item]))

    return item_sets, transaction_list


def get_freq_item_sets(item_set, transaction_list, min_support):
    _item_set = set()  # rezulta itemsets care sunt frecvente -> va fi returnat
    _item_dict = defaultdict(int)  # mapeaza [itemset : nrAparitii]

    for item in item_set:
        for transaction in transaction_list:  # parcurge item-ele din item_set prin toate tranzactiile...
            if item.issubset(transaction):  # si verifica daca apartine vreunei tranzactii
                _item_dict[item] += 1

    for item in _item_dict:
        if _item_dict[item] >= min_support:  # verifica daca item-ele din itemset sunt frecvente
            _item_set.add(item)

    return _item_set


def join_set(item_set, length):
    return set([i1.union(i2) for i1 in item_set for i2 in item_set if len(i1.union(i2)) == length])


def get_freq(records, min_support):
    result_dict = dict()
    one_element_item_sets, transactions = get_items_and_transaction_list(
        records)  # aflta toate itemset-urile de lungime 1 (adica C1)
    freq_one_element_item_sets = get_freq_item_sets(one_element_item_sets, transactions,
                                                    min_support)  # afla toate itemset-urile unitare frecvente (adica L1)
    current_freq_item_sets = freq_one_element_item_sets  # L1 = C1

    k = 2
    while current_freq_item_sets != set([]):
        result_dict[k - 1] = current_freq_item_sets  # adaug L(k-1) la totalul de de itemset-uri frecvente
        current_item_sets = join_set(current_freq_item_sets, k)  # aflu Ck
        current_freq_item_sets = get_freq_item_sets(current_item_sets, transactions, min_support)  # aflu Lk
        k = k + 1  # voi trece la aflarea L(k+1)

    return result_dict


def get_freq_items(start_date, no_of_days, min_support):
    utility = util.Utility()
    print("Getting frequent patterns...*")
    list_of_dict = []
    current_date, time_zone = du.get_date_from_elk_date_format(start_date)
    new_date = current_date

    for i in range(no_of_days):
        # records = elk.get_logs_final(start_date)
        records = con.get_complete_logs_dos(start_date)
        results = get_freq(records, min_support)

        # records = elk.get_logs_final(start_date)

        records = con.get_complete_logs_dos(start_date)
        cur_date = du.get_date_from_elk_date_format(start_date)[0]

        _date = cur_date.strftime("%d-%m-%Y")
        utility.get_ip_callers(results, records, _date)

        new_date = du.get_date_after(new_date, 1)
        start_date = du.get_elk_date_format_from_date(new_date, time_zone)
        list_of_dict.append(results)
    print("Completed: Found frequent patterns")
    return list_of_dict


if __name__ == '__main__':
    all_freq_item_sets = get_freq_items("2019-09-22T21:00:00.000Z", 5, 200)
