#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2011, IDA, Linköping University
# Copyright (C) 2011, Torbjörn Lönnemark <tobbez@ryara.net>
# Copyright (C) 2014, Daniel Persson
import json
import os
import random
import string
import unittest
import data  # import the file with your implemented functions
import hashlib
import sys
from operator import itemgetter


# ----------- HELPER FUNCTIONS -----------

def print_tech_dict(d):
    for k, v in d.items():
        print("{}: {}".format(k, v))
        for e in v:
            print(e)
        print()


def sort_dict(d, sort_key):
    for k in d.keys():
        d[k] = sorted(d[k], key=itemgetter(sort_key))
    return d


"""
Convenience function for creating a temporary `data.json` file.
`contents` should be a string with the contents the file should have.
`func` is a function taking one argument: the filename.
All tests using the file should occur in the function passed in as an argument
"""


def with_data_file(contents, func):
    while True:
        filename = ''.join(random.choices(string.ascii_letters, k=20)) + ".json"
        if not os.path.exists(filename):
            break

    file_created = False
    try:
        with open(filename, "x") as f:
            file_created = True
            f.write(contents)
        func(filename)
    finally:
        if file_created:
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass


md5 = hashlib.md5


# ----------- TEST CLASS -----------

class DataTest(unittest.TestCase):
    """ Subclass of the unittest.TestCase class

    Define all tests as a method of this class. Each test must start with the
    word test (ex test_load). Within each test method, various assertions
    can be made, e.g. checking that what you are testing gives the expected
    result.

    Use the method self.assertEqual() to compare an expected and observed result.

    Please refer to the unittest documentation for more information:
    https://docs.python.org/3.7/library/unittest.html

    To run the tests, have the files data_test.py, data.py and data.json in the
    same catalog. data.py is the file with your implemented API functions.
    Execute with:

    $ python3 data_test.py

    The test result is shown in the terminal.

    """

    def setUp(self):
        """ The setUp() method is called before every test_*-method. Use it to
        prepare things that must always be done before a test is run, such as
        loading the data.
        """

        # The content in self.expected_data must match the content in data.json
        # for the testing to work. Do NOT change the content or the file!
        self.expected_data = [{'big_image': 'XXX',
                               'project_name': 'python data-module test script',
                               'course_name': 'OK\xc4NT',
                               'group_size': 2, 'end_date': '2009-09-06',
                               'techniques_used': ['python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_id': 1,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-05',
                               'lulz_had': 'many'},
                              {'big_image': 'XXX',
                               'project_name': 'NEJ',
                               'course_name': 'OK\xc4NT',
                               'group_size': 4,
                               'end_date': '2009-09-08',
                               'techniques_used': ['c++', 'csv', 'python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_id': 3,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-07',
                               'lulz_had': 'few'},
                              {'big_image': 'XXX',
                               'project_name': '2007',
                               'course_name': 'OK\xc4NT',
                               'group_size': 6,
                               'end_date': '2009-09-09',
                               'techniques_used': ['ada', 'python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_id': 2,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-08',
                               'lulz_had': 'medium'},
                              {'big_image': 'XXX',
                               'project_name': ',',
                               'course_name': 'HOHO',
                               'group_size': 8,
                               'end_date': '2009-09-07',
                               'techniques_used': [],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': ' "',
                               'project_id': 4,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-06',
                               'lulz_had': 'over 9000'}
                              ]

        # Sort the expected data by project id
        self.expected_data = sorted(self.expected_data, key=itemgetter('project_id'))

        # Store the hardcoded expected results.
        # Do NOT change this part
        self.expected_technique_data = ['ada', 'c++', 'csv', 'python']
        self.expected_technique_stat_data = {'python': [{'id': 2, 'name': '2007'},
                                                        {'id': 3, 'name': 'NEJ'},
                                                        {'id': 1, 'name': 'python data-module test script'}],
                                             'csv': [{'id': 3, 'name': 'NEJ'}],
                                             'c++': [{'id': 3, 'name': 'NEJ'}],
                                             'ada': [{'id': 2, 'name': '2007'}]}

        # Load the data using your implemented load function. The data is
        # stored as a member of the class instance, so that it can be accessed
        # in other methods of the class
        self.loaded_data = sorted(data.load("data.json"), key=itemgetter('project_id'))

    def test_load(self):
        """ Test the implemented load function """

        # Compare the loaded data with the expected data
        self.assertEqual(self.loaded_data[0], self.expected_data[0])

        # Test that loading a non-existing file returns None
        self.assertEqual(data.load("/dev/this_file_does_not_exist"), None)

    def test_load_gives_sorted_data(self):
        """Test that the load function returns data sorted after project_id"""

        self.assertEqual(self.expected_data, data.load("data.json"))

    def test_load_ignores_duplicate_id(self):
        """Test that makes sure projects with duplicate project_id are ignored"""
        contents = [{
            'project_id': 1,
            'project_name': 'test',
            'techniques_used': []
        },
            {
                'project_id': 1,
                'project_name': 'test2',
                'techniques_used': []
            },
            {
                'project_id': 2,
                'project_name': 'test3',
                'techniques_used': []
            },
            {
                'project_id': 3,
                'project_name': 'test4',
                'techniques_used': []
            },
            {
                'project_id': 2,
                'project_name': 'test5',
                'techniques_used': []
            }]

        contents = json.dumps(contents)

        expected_contents = [{
            'project_id': 1,
            'project_name': 'test',
            'techniques_used': []
        },
            {
                'project_id': 2,
                'project_name': 'test3',
                'techniques_used': []
            },
            {
                'project_id': 3,
                'project_name': 'test4',
                'techniques_used': []
            }]

        with_data_file(contents, lambda x: self.assertEqual(data.load(x), expected_contents))

    def test_reload(self):
        """ Test that the load function reads the file again, and doesn't return old data """

        expected_data_1 = [{
            'project_id': 1,
            'project_name': 'test',
            'techniques_used': []
        }]
        expected_data_2 = [{
            'project_id': 1000,
            'project_name': 'test_2',
            'techniques_used': ['woooo']
        }]

        # We should not leave `data2.json` alive, even if an assertion failed
        try:
            # We also need to test with two different contents,
            # to disallow caching based on file name
            with open("data2.json", "w") as f:
                json.dump(expected_data_1, f)

            self.assertEqual(data.load("data2.json"), expected_data_1)

            with open("data2.json", "w") as f:
                json.dump(expected_data_2, f)

            self.assertEqual(data.load("data2.json"), expected_data_2)
        finally:
            # Remove `data2.json`, and do not error if it doesn't exist.
            # Using `os.path.exists` may create a race condition,
            # as the file can be removed between the calls to `exists`
            # and `remove`.
            try:
                os.remove("data2.json")
            except FileNotFoundError:
                pass

    def test_get_project_count(self):
        """ Test the implemented function get_project_count """

        # Test that the correct number of projects are returned
        self.assertEqual(data.get_project_count(self.loaded_data), 4)

    def test_get_project(self):
        """ Test the implemented function get_project """

        # Try to get project 1, 2, 3 and 4 and check that a project with
        # the correct project_id is returned.
        self.assertEqual(data.get_project(self.loaded_data, 1)['project_id'], 1)
        self.assertEqual(data.get_project(self.loaded_data, 2)['project_id'], 2)
        self.assertEqual(data.get_project(self.loaded_data, 3)['project_id'], 3)
        self.assertEqual(data.get_project(self.loaded_data, 4)['project_id'], 4)

        # Try to get a non-existing project and check that None is returned
        self.assertEqual(data.get_project(self.loaded_data, 42), None)

    def test_search_all(self):
        """ Test than an empty search query returns all projects """

        # Due to these not containing the field being sorted by,
        # they should be ordered by project ID.
        contents = [{
            "project_id": 2,
            "project_name": "Discord",
            "techniques_used": ["html", "css"]
        }, {
            "project_id": 1,
            "project_name": "Web Browser",
            "techniques_used": ["c++", "duct dape"]
        }, {
            "project_id": 1337,
            "project_name": "",
            "techniques_used": []
        }]

        expected = [{
            "project_id": 1,
            "project_name": "Web Browser",
            "techniques_used": ["c++", "duct dape"]
        }, {
            "project_id": 2,
            "project_name": "Discord",
            "techniques_used": ["html", "css"]
        }, {
            "project_id": 1337,
            "project_name": "",
            "techniques_used": []
        }]

        with_data_file(json.dumps(contents), lambda f: self.assertEqual(data.search(data.load(f)), expected))


    def test_search_filter(self):
        contents = [
            {"project_id": 1,  "project_name": "Project 1",  "techniques_used": []},
            {"project_id": 2,  "project_name": "Project 2",  "techniques_used": ["abc"]},
            {"project_id": 3,  "project_name": "Project 3",  "techniques_used": ["abc", "def"]},
            {"project_id": 4,  "project_name": "Project 4",  "techniques_used": ["これから本番だ", "def"]},
            {"project_id": 5,  "project_name": "Project 5",  "techniques_used": []},
            {"project_id": 6,  "project_name": "Project 6",  "techniques_used": ["\x1b[31mwhat\x1b[0m"]},
            {"project_id": 7,  "project_name": "Project 7",  "techniques_used": ["övrigt", "c++"]},
            {"project_id": 8,  "project_name": "Project 8",  "techniques_used": ["c++", "css"]},
            {"project_id": 9,  "project_name": "Project 9",  "techniques_used": ["c++", "git", "def"]},
            {"project_id": 10, "project_name": "Project 10", "techniques_used": ["scratch", "rust"]},
            {"project_id": 10, "project_name": "Project 10", "techniques_used": ["\x00Test"]},
        ]

        self.assertEqual(data.search(contents, techniques=[]), contents)
        self.assertEqual(data.search(contents, techniques=["abc"]), [
            {"project_id": 2,  "project_name": "Project 2",  "techniques_used": ["abc"]},
            {"project_id": 3,  "project_name": "Project 3",  "techniques_used": ["abc", "def"]},
        ])
        self.assertEqual(data.search(contents, techniques=["def"]), [
            {"project_id": 3,  "project_name": "Project 3",  "techniques_used": ["abc", "def"]},
            {"project_id": 4,  "project_name": "Project 4",  "techniques_used": ["これから本番だ", "def"]},
            {"project_id": 9,  "project_name": "Project 9",  "techniques_used": ["c++", "git", "def"]},
        ])
        self.assertEqual(data.search(contents, techniques=["abc", "def"]), [
            {"project_id": 3,  "project_name": "Project 3",  "techniques_used": ["abc", "def"]},
        ])
        self.assertEqual(data.search(contents, techniques=["abc", "def", "rust"]), [
        ])
        self.assertEqual(data.search(contents, techniques=["本番"]), [
        ])
        self.assertEqual(data.search(contents, techniques=["\x1b[31mwhat\x1b[0m"]), [
            {"project_id": 6,  "project_name": "Project 6",  "techniques_used": ["\x1b[31mwhat\x1b[0m"]},
        ])
        self.assertEqual(data.search(contents, techniques=["\\x1b]31what\\x1b[0m"]), [
        ])
        self.assertEqual(data.search(contents, techniques=["c++"]), [
            {"project_id": 7,  "project_name": "Project 7",  "techniques_used": ["övrigt", "c++"]},
            {"project_id": 8,  "project_name": "Project 8",  "techniques_used": ["c++", "css"]},
            {"project_id": 9,  "project_name": "Project 9",  "techniques_used": ["c++", "git", "def"]},
        ])
        self.assertEqual(data.search(contents, techniques=["c++"]), [
            {"project_id": 7,  "project_name": "Project 7",  "techniques_used": ["övrigt", "c++"]},
            {"project_id": 8,  "project_name": "Project 8",  "techniques_used": ["c++", "css"]},
            {"project_id": 9,  "project_name": "Project 9",  "techniques_used": ["c++", "git", "def"]},
        ])
        self.assertEqual(data.search(contents, techniques=["\x00Test"]), [
            {"project_id": 10, "project_name": "Project 10", "techniques_used": ["\x00Test"]},
        ])
        self.assertEqual(data.search(contents, techniques=["\x00Testing"]), [
        ])


    def test_search(self):
        """ Test the implemented search function """

        # Call search with no other parameters than the database.
        # All projects should be returned
        self.assertEqual(len(data.search(self.loaded_data)), 4)

        # Search for projects with csv as technique.
        # 1 project should be returned
        self.assertEqual(len(data.search(self.loaded_data, techniques=['csv'])), 1)

        # Search for projects including Python and sort them in ascending order.
        # Ensure that returned projects are sorted by ascending dates
        res = data.search(self.loaded_data, sort_order='asc', techniques=["python"])
        self.assertEqual(res[0]['start_date'], '2009-09-05')
        self.assertEqual(res[1]['start_date'], '2009-09-07')
        self.assertEqual(res[2]['start_date'], '2009-09-08')

        # Search for the term 'okänt' in three specified search fields. Sort
        # results by end_date.
        # Ensure that projects are returned in the correct order.
        res = data.search(self.loaded_data,
                          sort_by="end_date",
                          search='okänt',
                          search_fields=['project_id', 'project_name', 'course_name'])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]['project_id'], 2)
        self.assertEqual(res[1]['project_id'], 3)
        self.assertEqual(res[2]['project_id'], 1)

        # Search for 'okänt' in specified search fields.
        # Ensure correct number of results
        res = data.search(self.loaded_data,
                          search="okänt",
                          search_fields=["project_id", "project_name", "course_name"])
        self.assertEqual(len(res), 3)

        # Search for 'okänt' in specified search fields, provide empty technique list
        # Ensure correct number of results
        res = data.search(self.loaded_data,
                          techniques=[],
                          search="okänt",
                          search_fields=["project_id", "project_name", "course_name"])
        self.assertEqual(len(res), 3)

        # Search for 'okänt', provide empty search fields list
        # Ensure 0 results
        res = data.search(self.loaded_data, search="okänt", search_fields=[])
        self.assertEqual(len(res), 0)

        # Search with results sorted by group size.
        # Ensure results are in descending order
        res = data.search(self.loaded_data, sort_by='group_size')
        self.assertEqual(res[0]['project_id'], 4)  # 1
        self.assertEqual(res[1]['project_id'], 2)  # 2
        self.assertEqual(res[2]['project_id'], 3)  # 3
        self.assertEqual(res[3]['project_id'], 1)  # 4


    def test_case_insensitive_search(self):
        """Test that makes sure that search case-insensive even if search-input is not """
        contents = [{
            'project_id': 1,
            'project_name': 'Test',
            'start_date': '2009-09-07',
            'techniques_used': []
        },
            {
                'project_id': 2,
                'project_name': 'TEST',
                'start_date': '2009-09-07',
                'techniques_used': []
            },
            {
                'project_id': 3,
                'project_name': 'test',
                'start_date': '2009-09-07',
                'techniques_used': []
            },
            {
                'project_id': 4,
                'project_name': 'TeSt',
                'start_date': '2009-09-07',
                'techniques_used': []
            }]

        #should include all projects 1-4
        expected_contents = [{
            'project_id': 1,
            'project_name': 'Test',
            'start_date': '2009-09-07',
            'techniques_used': []
        },
            {
                'project_id': 2,
                'project_name': 'TEST',
                'start_date': '2009-09-07',
                'techniques_used': []
            },
            {
                'project_id': 3,
                'project_name': 'test',
                'start_date': '2009-09-07',
                'techniques_used': []
            },
            {
                'project_id': 4,
                'project_name': 'TeSt',
                'start_date': '2009-09-07',
                'techniques_used': []
            }]

        self.assertEqual(expected_contents, data.search(contents, search="Test",search_fields=["project_name"]))
        self.assertEqual(expected_contents, data.search(contents, search="TEST",search_fields=["project_name"]))
        self.assertEqual(expected_contents, data.search(contents, search="test",search_fields=["project_name"]))
        self.assertEqual(expected_contents, data.search(contents, search="TeSt",search_fields=["project_name"]))

    def test_search_places_non_existant_sort_by_fields_last(self):
        """ Test that makes sure that projects lacking the field specified in sort_by are placed last when calling the search function """
        contents = [{
            'project_id': 1,
            'project_name': 'test',
            'techniques_used': [],
            'short_description': 'bsdf'
        },
            {
                'project_id': 2,
                'project_name': 'test2',
                'techniques_used': []
            },
            {
                'project_id': 3,
                'project_name': 'test3',
                'techniques_used': [],
                'short_description': 'asdf'
            },
            {
                'project_id': 4,
                'project_name': 'test4',
                'techniques_used': []
            }, ]

        # since both test2 and test4 lack a short_description, sort them by project_id
        expected_contents = [{
            'project_id': 3,
            'project_name': 'test3',
            'techniques_used': [],
            'short_description': 'asdf'
        },
            {
                'project_id': 1,
                'project_name': 'test',
                'techniques_used': [],
                'short_description': 'bsdf'
            },
            {
                'project_id': 2,
                'project_name': 'test2',
                'techniques_used': []
            },
            {
                'project_id': 4,
                'project_name': 'test4',
                'techniques_used': []
            }]

        self.assertEqual(expected_contents, data.search(contents, sort_by="short_description", sort_order="asc"))

    def test_search_sort_order_is_valid(self):
        """ Test that makes sure search raises ValueError if sort order is not 'desc' or 'asc' """
        self.assertRaises(ValueError, data.search, self.loaded_data, sort_order="asdf")

    def test_search_invalid_comparison(self):
        """ Test that make sures search raises TypeError if field specified in sort_by can not be compared """

        contents = [{
            'project_id': 1,
            'project_name': 'test',
            'techniques_used': [],
            'field_to_compare': 'hello'
        },
        {
            'project_id': 2,
            'project_name': 'test2',
            'techniques_used': [],
            'field_to_compare': 9999
        }]

        self.assertRaises(TypeError, data.search, contents, sort_by='field_to_compare')

        # changes 'field_to_compare' to an empty dict (not comparable) on both projects
        contents[0]['field_to_compare'], contents[1]['field_to_compare'] = {}, {}

        self.assertRaises(TypeError, data.search, contents, sort_by='field_to_compare')

    def test_get_techniques(self):
        """ Test the implemented get_techniques function """

        res = data.get_techniques(self.loaded_data)
        self.assertEqual(res, self.expected_technique_data)

    def test_get_technique_stats(self):
        """ Test the implemented get_technique_stats function """

        res = data.get_technique_stats(self.loaded_data)
        res = sort_dict(res, 'id')

        self.expected_technique_stat_data = sort_dict(self.expected_technique_stat_data, 'id')

        self.assertEqual(res, self.expected_technique_stat_data)


if __name__ == '__main__':
    print("Test:     ", md5(sys.argv[0].encode('UTF-8')).hexdigest())
    print("Test data:", md5(b"data.json").hexdigest())
    print()
    unittest.main()
