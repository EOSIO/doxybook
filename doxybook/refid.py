import re
"""
Some refid might include additional suffix, i.e.
classeosio_1_1multi__index_a421ef78ccdc84f0f6b2b14e2732527ba_1a421ef78ccdc84f0f6b2b14e2732527ba
or group__contract_ga7e3b8d6376c0895402569e4bc275a526_1ga7e3b8d6376c0895402569e4bc275a526
or classeosio_1_1multi__index_a421ef78ccdc84f0f6b2b14e2732527ba
or group__contract_ga7e3b8d6376c0895402569e4bc275a52
or structeosio_1_1indexed__by_ad04dd8d771430edeb499c9d03bc9bb60_1ad04dd8d771430edeb499c9d03bc9bb60a4645263158ffe7d237fda11ac37aea05
or might be nothing at all i.e. classeosio_1_1multi__index
which can't be used to refer to another markdown file and messes up the cache 
This kind of refid needs to be normalize into single format
"""
def normalize_refid(refid: str):
    splitted_refid = refid.split('_')
    len_of_splitted_refid = len(splitted_refid)
    for _ in range (0, min(2, len_of_splitted_refid)):
        refid_tail = splitted_refid[-1]
        refid_tail_len = len(refid_tail)
        is_len_within_member_id_range = ((refid_tail_len >= 33 and refid_tail_len <= 35) or (refid_tail_len >= 67 and refid_tail_len <= 68))
        is_content_within_member_id_range = re.search(r'^[0-9a-g]+$', refid_tail) 
        is_tail_member_id = is_len_within_member_id_range and is_content_within_member_id_range
        if is_tail_member_id:
            # Remove tail from the splitted refid
            splitted_refid.pop()
    normalized_refid = '_'.join(splitted_refid)
    return normalized_refid