import re

"""
Even though a doxygen xml node refers to the same another doxygen xml node, occasionally the refid is not the same
Some refid might include member id suffix more than once, i.e.
classeosio_1_1multi__index_a421ef78ccdc84f0f6b2b14e2732527ba and
classeosio_1_1multi__index_a421ef78ccdc84f0f6b2b14e2732527ba_1a421ef78ccdc84f0f6b2b14e2732527ba
or
group__contract_ga7e3b8d6376c0895402569e4bc275a526 and
group__contract_ga7e3b8d6376c0895402569e4bc275a526_1ga7e3b8d6376c0895402569e4bc275a526
or
structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60 and
structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60 and
structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05
This messes up the reference to another doxygen xml node, and hence to make it consistent they need to be normalized into a single format
The decided format is the one with single member id, i.e. group__contract_ga7e3b8d6376c0895402569e4bc275a52

This helper function will be used to normalize the refid into a single format
"""
def normalize_refid(refid: str):
    refid_prefix, member_id_list = split_member_id_from_refid(refid)
    normalized_refid = refid_prefix
    if len(member_id_list) > 0:
      normalized_refid += '_' + member_id_list[0]
    return normalized_refid

"""
This is a helper function that is used to get the refid prefix, in other words refid without the member id
e.g.
With the input of structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05
it will return "structeosio_1_1indexed__by"
"""
def extract_refid_prefix(refid: str):
    refid_prefix, _ = split_member_id_from_refid(refid)
    return refid_prefix

"""
This is a helper function that is used to either get the refid prefix or normalize the refid
This will return a tuple of refid prefix and the list of member id extracted
e.g.
With the input of structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05
it will return ("structeosio_1_1indexed__by", ["ad04dd8d771430edeb499c9d03bc9bb60", "1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05"])
"""
def split_member_id_from_refid(refid: str):
    member_id_list = []
    splitted_refid = refid.split('_')
    len_of_splitted_refid = len(splitted_refid)
    # No need to check the first element
    for _ in range (0, min(2, len_of_splitted_refid)):
        refid_tail = splitted_refid[-1]
        if is_member_id(refid_tail):
            # Remove tail from the splitted refid
            member_id = splitted_refid.pop()
            # And record it in the list
            member_id_list.insert(0, member_id)
    refid_prefix = '_'.join(splitted_refid)
    return refid_prefix, member_id_list

"""
Test if a string is a member id, i.e.
ad04dd8d771430edeb499c9d03bc9bb60 or 1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05 in
structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05
The criteria is, the text is between 33-35 or 67-68 and it only consists 0-9 and a-g
"""
def is_member_id(str_to_test: str):
    len_of_str_to_test = len(str_to_test)
    is_len_within_member_id_range = ((len_of_str_to_test >= 33 and len_of_str_to_test <= 35) or (len_of_str_to_test >= 67 and len_of_str_to_test <= 68))
    is_content_within_member_id_range = re.search(r'^[0-9a-g]+$', str_to_test)
    return is_len_within_member_id_range and is_content_within_member_id_range
