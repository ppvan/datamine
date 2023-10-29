from typing import List
from datatypes import Record


def flatten_list(list_of_list: List[List]) -> List:
    return [item for sublist in list_of_list for item in sublist]


def dupplicate_record_by_quintuple(record: Record) -> List[Record]:
    """
    If a record have mutiple quintuples, duplicate it to a list of record, each have 1 quintuple
    """

    result = []

    for quintuple in record.quintuples:
        record_copy = record
        record_copy.quintuples = [quintuple]
        result.append(record_copy)

    return result
