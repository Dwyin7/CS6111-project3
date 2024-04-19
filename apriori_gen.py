import itertools
import collections

# L_k_1 is an ordered lists of itemsets
"""
Input: L_k_1 is a list of list
Return: C_k as a list of list
Here we dont need to order.
"""


def apriori_gen_with_prune(L_k_1):
    c_k = []

    for i in range(len(L_k_1)):
        for j in range(i + 1, len(L_k_1)):
            if L_k_1[i][:-1] == L_k_1[j][:-1] and L_k_1[i][-1] < L_k_1[j][-1]:
                cand = L_k_1[i] + [L_k_1[j][-1]]
                # Prune
                """Iterate candidate in C_k Check if subset(size k-1) of candidate not in original L_k_1, then remove the candidate. """
                if not any(
                    list(subset) not in L_k_1
                    for subset in itertools.combinations(cand, len(cand) - 1)
                ):
                    c_k.append(cand)

    return c_k


def calculate_conf(res_idxs, conf):
    cand_dict = collections.defaultdict(int)
    for lst in res_idxs:
        for ele in lst:
            cand_dict[tuple(ele[0])] = ele[1]
    # print(cand_dict)
    # for key in cand_dict.keys():
    #     print(key, cand_dict[key])

    rules = collections.defaultdict(int)
    for l_n in res_idxs:
        # print(" =========")
        if len(l_n) == 0 or len(l_n[0][0]) == 1:
            continue
        for cand in l_n:
            for subset in itertools.combinations(cand[0], len(cand[0]) - 1):
                # print(subset)
                s_cand = set(tuple(cand[0]))
                s_cand_supp = cand[1]  # float
                s_subset = set(subset)
                diff = s_cand - s_subset

                right = tuple(diff)

                # left = list(diff)[0]
                # print("word....")
                # print(left)
                # print(cand_dict[tuple(left)])
                # print(cand_dict[tuple(cand[0])])
                comp_conf = cand[1] / cand_dict[subset]
                if comp_conf >= conf:
                    # print("subset",subset, cand)
                    # print(diff,"testdiff")
                    # print(right)
                    rule = subset + right

                    # print(rule)
                    # print("=======")
                    # print(comp_conf)
                    rules[rule] = (comp_conf, s_cand_supp)
    return rules


# Testing
# L_k_minus_1 = [['1', '2','3'], ['1','2','4'], ['1','3','4'], ['1','3','5'], ['2','3','4']] #['1', '2', '3', '4']
# # L_k_minus_1 = [['1'],['2'],['3']]
# C_k = apriori_gen_with_prune(L_k_minus_1)
# print(C_k)
# print(type(C_k))
