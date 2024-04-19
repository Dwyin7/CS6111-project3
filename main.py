import pandas as pd
import sys
import collections
from apriori_gen import apriori_gen_with_prune, calculate_conf


def init_l1(supp, data):
    # return list of (itemset, supp)
    length = len(data)
    supports = data.sum() / length
    filtered_col_names = supports[supports >= supp].index.tolist()
    # return [[item, supports[item]] for item in filtered_col_names]
    return [[[item], supports[item]] for item in filtered_col_names]


def remove_supp(li):
    return [item[0] for item in li]


def apriori(l1, baseket, supp):
    # l1: [[id],...]

    # res stores [l1,l2,...]
    res = [l1]
    while len(res[-1]) > 0:
        raw_li = remove_supp(res[-1])
        ck = apriori_gen_with_prune(raw_li)
        # print("ck length: ", len(ck))
        mp = collections.defaultdict(int)
        for t in baseket:
            ct = subset(ck, t)
            for c in ct:
                mp[tuple(c)] += 1
        items = mp.items()
        lk = [
            [list(k), v / len(baseket)] for k, v in items if v >= len(baseket) * supp
        ]  # tuple list
        # print("lk length: ", len(lk))
        res.append(lk)
        # print("result length :", len(res))
    return res


def print_list(lst):
    s = ",".join(lst)
    return f"[{s}]"


def subset(ck, t: list):
    # t is the transcations
    # set of set
    t = set(t)
    res = []
    for tp in ck:
        stp = set(tp)
        if stp.issubset(t):
            res.append(tp)
    return res


def get_basket(data):
    temp = data.values.tolist()
    basket = []
    for idxs in temp:
        basket.append([idx for idx, t in enumerate(idxs) if t])
    return basket


def test():
    data = [
        ["pen", "ink", "diary", "soap"],
        ["pen", "ink", "diary"],
        ["pen", "diary"],
        ["pen", "ink", "soap"],
    ]
    df = pd.DataFrame(data)

    def expand_row(row):
        return pd.Series({item: True for item in row if pd.notna(item)})

    one_hot_encoded_df = df.apply(expand_row, axis=1).fillna(False)
    return one_hot_encoded_df


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <dataset_file> <param1> <param2>")
        return
    dataset_file = sys.argv[1]
    supp = float(sys.argv[2])
    conf = float(sys.argv[3])

    dataset_file = "INTEGRATED-DATASET.csv"

    df = pd.read_csv(dataset_file)

    # df = test()

    headers = list(df.columns)
    # print("header length", len(headers), headers)

    # change col name
    new_column_names = {
        old_name: int(index) for index, old_name in enumerate(df.columns)
    }
    df.rename(columns=new_column_names, inplace=True)
    l1 = init_l1(supp, df)

    baseket = get_basket(df)

    res_idxs = apriori(l1, baseket, supp)
    res = []
    for li in res_idxs:
        temp = []
        for lj in li:
            temp2 = []
            for i in lj[0]:
                temp2.append(headers[i])
            temp.append([temp2, lj[1]])
        if not temp:
            break
        res.append(temp)

    print("start testing.....")
    print(f"==Frequent itemsets (min_sup={supp*100}%")
    conf_rules = []
    for li in res:
        for its in li:
            conf_rules.append(its)
    ordered_conf_rules = sorted(conf_rules, key=lambda x: x[1], reverse=True)
    for rule in ordered_conf_rules:
        print(f"{print_list(rule[0])}, {rule[1]*100}%")

    rules = calculate_conf(res_idxs, conf)

    ordered_rules = list(rules.items())
    ordered_rules = sorted(ordered_rules, key=lambda x: x[1], reverse=True)

    print(f" \n\n==High-confidence association rules (min_conf={conf*100}%)")
    for key in ordered_rules:
        print(
            f"{print_list([headers[i] for i in key[0][:-1]])} => [{headers[key[0][-1]]}]  (Conf:{key[1][0]*100}%, Supp:{key[1][1]*100}%)"
        )


if __name__ == "__main__":
    main()
