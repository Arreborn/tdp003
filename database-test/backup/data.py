#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def load(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def get_project_count(db):
    return len(db)


def get_project(db, id):
    temp = filter(lambda k: (k["project_id"] == id), db)
    for i in temp:
        return i


def get_techniques(db):
    return_list = []

    for i in db:
        for j in i["techniques_used"]:
            if j not in return_list:
                return_list.append(j)

    return_list.sort()
    return return_list


def get_technique_stats(db):
    techs = get_techniques(db)
    return_dict = dict.fromkeys(techs)
    for i in db:
        temp = {"id": i["project_id"], "name": i["project_name"]}
        for j in i["techniques_used"]:
            if return_dict[j] == None:
                return_dict[j] = [temp]
            else:
                return_dict[j].append(temp)

    return return_dict


def search(
    db,
    sort_by="start_date",
    sort_order="desc",
    techniques=None,
    search=None,
    search_fields=None,
):
    return_list = []

    # Fel - i testerna skickas det in fler search_fields än bara ett i en lista, så vi behöver
    # rätta till så att den funkar

    for i in db:
        check_tech = False
        check_search = False

        # if techniques != None and len(techniques) != 0:
        if techniques != None:
            # Tar vi bort denna extra if-sats och lägger den ovan funkar inte testerna. Varför?
            if len(techniques) != 0:
                for j in techniques:
                    if j in i["techniques_used"]:
                        check_tech = True
            else:
                check_tech = True
        elif techniques == None:
            check_tech = True

        if search != None:
            if search_fields != None:
                for j in search_fields:
                    if search == i[j]:
                        check_search = True
            else:
                if search in i.values():
                    check_search = True

        elif search == None:
            check_search = True

        if check_tech == True and check_search == True:
            return_list.append(i)

    if sort_order == "desc":
        return_list = sorted(return_list, key=lambda k: k[sort_by], reverse=True)

    elif sort_order == "asc":
        return_list = sorted(return_list, key=lambda k: k[sort_by])

    return return_list


# if __name__ == "__main__":

#     db = load("data.json")

#     #     # print(get_project_count(db))

#     #     # print(get_project(db, 4))

#     #     # print(get_techniques(db))

#     #     # temp = get_techniques_stats(db)

#     #     # print(temp)

#     temp = search(
#         db,
#         sort_by="end_date",
#         search="OKÄNT",
#         search_fields=["project_id", "project_name", "course_name"],
#     )
#     for i in temp:
#         print(i)
#         print("")
#         print("----")
#         print("")
