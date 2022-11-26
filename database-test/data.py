#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# In order to handle the file data.json the appropriate module is required
import json

# ----- data.load(path to data.json) -----
# The load-function loads all data from data.json and returns a list of dictionaries
# Please observe that the function only accepts .json files!
# This function also ensures no data from data.json missing the required fields will not be loaded
# Required fields are project_id, project_name and techniques
# Finally, the load function also ensures no projects with identical id is loaded together as only the first instance of an unique id is appended to the list
# The returned database is sorted by the projects start date
#
# If the filename is incorrect, the function raises a FileNotFoundError


def load(filename):
    try:
        with open(filename, encoding="utf-8") as file:
            data_file = json.load(file)

            added_projects = []
            found_projects = []

            # i stands for the current project in the data.json-file that is currently being processed
            for i in range(len(data_file)):
                if (
                    "project_id" in dict.keys(data_file[i])
                    and "project_name" in dict.keys(data_file[i])
                    and "techniques_used" in dict.keys(data_file[i])
                ):
                    if data_file[i]["project_id"] not in added_projects:
                        found_projects.append(data_file[i])
                        added_projects.append(data_file[i]["project_id"])

            found_projects = sorted(found_projects, key=lambda k: k["start_date"])
            return found_projects

    except FileNotFoundError:
        return None


# ----- data.get_project_count(list of dictionaries) -----
# This function accepts the list loaded from data.load, and returns the number of projects available in the database


def get_project_count(db):
    return len(db)


# ----- data.get_project(list of dictionaries, int) -----
# This function accepts the database and one unique project id
# Returns the dictionary with the specified project id


def get_project(db, id):
    # where k stands for key
    filter_for_project_id = filter(lambda k: (k["project_id"] == id), db)
    for correct_project in filter_for_project_id:
        return correct_project


# ----- get_techniques('database from data.json') -----
# This function accepts the database loaded from data.json
# The function returns a list of all techniques found across all projects
# Currently, the function does not check for correct capitalization and will return both 'JAVA', 'Java' and 'java' if they occur in data.json
# Please ensure all techniques in data.json are formatted and capitalized accordingly


def get_techniques(db):
    techs_used = []

    for project in db:
        for techniques in project["techniques_used"]:
            if techniques not in techs_used:
                techs_used.append(techniques)

    techs_used.sort()
    return techs_used


# ----- data.get_technique_stats(list of dictionaries)
# This function accepts the database loaded fro data.json
# Returns a list with dictionaries, where each key relates to onec
# individual technique used in a project
# The value of each key is a list of dictionaries containing the project id and name of all projects using the current project in the dictionary key
# Currently, the function does not check for correct capitalization and will return both 'JAVA', 'Java' and 'java' if they occur in data.json
# Please ensure all techniques in data.json are formatted and capitalized accordingly


def get_technique_stats(db):
    techs = get_techniques(db)
    complete_dict = dict.fromkeys(techs)
    for project in db:
        project_id_and_name = {
            "id": project["project_id"],
            "name": project["project_name"],
        }
        for tech in project["techniques_used"]:
            if complete_dict[tech] == None:

                complete_dict[tech] = [project_id_and_name]
            else:
                complete_dict[tech].append(project_id_and_name)

    return complete_dict


# -----data.search(list of dictionaries, string, string, list, string, list) -----
# This function accepts several optional parameters to find specific projects in data.json
# The function returns a list containing dictionaries that contains the specified search parameters
# More details regarding the specifics of the search function can be found below in the functions code


def search(
    db,  # list of dictionaries
    sort_by="start_date",  # string
    sort_order="desc",  # string
    techniques=None,  # list
    search=None,  # string
    search_fields=None,  # list
):

    return_search = []

    if techniques == []:
        techniques = None

    for project in db:
        # These booleans check if the current project containts the parameters supplied to the function
        check_tech = False
        check_search = False

        # The code block below checks if the current project in the loop contains the techniques the user searched for, if found, the bool check_tech is set to true
        # If the user did not specify any techniques to search for, the code block does not execute and the bool is set to true by default
        if techniques != None:

            if len(techniques) != 0:
                length = len(techniques)
                for tech in techniques:
                    if tech in project["techniques_used"]:
                        length -= 1

                if length == 0:
                    check_tech = True

        elif techniques == None:
            check_tech = True

        # The code block below checks if the string search exists in the current project
        # If the function is supplied with a list in the variable search_fields, the function only checks if the search string exists in the specified fields
        # If the string is found (and if it is found in the specified search fields when applicable), the bool check_search is set to true
        # If the user did not enter a specific search field, the bool is set to true if the search string is found anywhere in the current project
        # If the user did not enter a specific search string, the bool is set to true by default
        if search != None:

            if search_fields != None:
                for value_of_search in search_fields:
                    if str(search).lower() in str(project[value_of_search]).lower():
                        check_search = True

            else:
                for value in project.values():
                    if search.lower() in str(value).lower():
                        check_search = True

        elif search == None:
            check_search = True

        # If both booleans are set to true, the current project contains both the techniques and the search string (in the specific search fields when applicable)
        # If both booleans are true, the project is added to the list that is returned at the end of the function
        if check_tech == True and check_search == True:
            return_search.append(project)

    # End of for-loop, at this point all projects in the database have been checked
    # Dictionaries that relate to the current search are now appended to the list return_search

    # The code block below sorts the list according to the specified sort order (when applicable)
    # If the function receives anything but "asc" or "desc" as the sort order, the function raises a ValueError
    if sort_order == "desc":
        try:
            return_search = sorted(
                return_search, key=lambda k: k[sort_by], reverse=True
            )
        except KeyError:
            return_search = sorted(
                return_search, key=lambda k: k["project_id"], reverse=True
            )

    elif sort_order == "asc":
        try:
            return_search = sorted(return_search, key=lambda k: k[sort_by])
        except KeyError:
            return_search = sorted(return_search, key=lambda k: k["project_id"])

    else:
        raise ValueError

    return return_search
