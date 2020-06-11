import multiprocessing as mp

from pkg_levenshtein import algorithms as lev
from pkg_elastic import fields as fd


def compute_string_fields(left, right, field: fd.Fields):
    field_name = field.value[0]
    if field_name in left and field_name not in right:
        left_res = left[field_name]
        right_res = '-'
    elif field_name not in left and field_name in right:
        left_res = '-'
        right_res = right[field_name]
    elif field_name not in left and field_name not in right:
        left_res = '-'
        right_res = '-'
    else:
        left_res = left[field_name]
        right_res = right[field_name]
    return left_res, right_res


def compute_integer_fields(left, right, field: fd.Fields):
    field_name = field.value[0]
    if field_name in left and field_name not in right:
        left_res = int(left[field_name])
        right_res = 1000
    elif field_name not in left and field_name in right:
        left_res = 1000
        right_res = int(right[field_name])
    elif field_name not in left and field_name not in right:
        left_res = 1000
        right_res = 1000
    else:
        left_res = int(left[field_name])
        right_res = int(right[field_name])
    return left_res, right_res


def compute_field(left_arg, right_arg, field: fd.Fields):
    if field == fd.Fields.Method or field == fd.Fields.Request or field == fd.Fields.Query:
        left, right = compute_string_fields(left_arg, right_arg, field)
        # return lev.compute_distance(left, right)
        return lev.compute_similarity(left, right)

    elif field == fd.Fields.Resp_Class or field == fd.Fields.Resp_Code or field == fd.Fields.Data_Transf:
        left, right = compute_integer_fields(left_arg, right_arg, field)
        return abs(left - right)


def get_matrix_for_dataset_parallel(dataset, field: fd.Fields):
    dim = len(dataset)
    dis_matrix = [[0.0] * dim for _ in range(dim)]

    pool = mp.Pool(mp.cpu_count())
    args = []
    indexes = []
    for i in range(dim):
        for j in range(dim):
            if i > j:
                args.append((dataset[i], dataset[j], field))
                indexes.append((i, j))
            else:
                break

    results = pool.starmap(compute_field, args)

    for index_tuple, result in zip(indexes, results):
        i, j = index_tuple
        res = result
        dis_matrix[i][j] = res
    return dis_matrix


def get_matrix_for_dataset_serial(dataset, field: fd.Fields):
    dimensions = len(dataset)
    dis_matrix = [[0.0] * dimensions for _ in range(dimensions)]

    elements = dataset

    for i in range(len(dataset)):
        for j in range(len(dataset)):
            if i > j:
                dis_matrix[i][j] = compute_field(elements[i], elements[j], field)
            else:
                break

    return dis_matrix


def get_matrix_for_dataset(dataset, field: fd.Fields):
    dim = len(dataset)
    if dim > 110:
        return get_matrix_for_dataset_parallel(dataset, field)
    else:
        return get_matrix_for_dataset_serial(dataset, field)
