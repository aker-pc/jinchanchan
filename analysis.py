import pandas as pd


hero_relations = []

def rec_info(heroes, hero_list, relation_dict):
    if len(hero_list) > 8:
        hero_relations.append((hero_list, relation_dict.keys()))
        print((hero_list, relation_dict.keys()))
        return
    for hero_key, hero_detail in heroes.items():
        hero_real_relations = hero_detail["relation"]
        if hero_key in hero_list:
            continue
        else:
            hero_list.append(hero_key)
            for h_rl in hero_real_relations.split("|"):
                if h_rl in relation_dict:
                    relation_dict[h_rl] = relation_dict[h_rl] + 1
                else:
                    relation_dict[h_rl] = 1
            rec_info(heroes, hero_list, relation_dict)
            hero_list.pop()
            for h_rl in hero_real_relations.split("|"):
                relation_dict[h_rl] = relation_dict[h_rl] - 1
                if not relation_dict[h_rl]:
                    del relation_dict[h_rl]


data = pd.read_csv("hero_info.csv")
data.set_index("name", inplace=True)
hero_dict = data.to_dict(orient="index")
rec_info(hero_dict, [], {})
print(hero_relations)
