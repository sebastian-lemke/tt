from __future__ import print_function

from collections import defaultdict

from tt.dateutils.dateutils import *
from tt.dataaccess.utils import get_data_store
from tt.actions.utils import reportingutils


def action_list(projectsOrTags):
    delim = ','
    data = get_data_store().load()
    work = data['work']

    # initialize a null list
    unique_list = []

    if 'projects' in projectsOrTags:
        print('List of all distinct projects:', sep='')

        for item in work:
            if 'end' in item:
                name = item['name']
                # check if exists in unique_list or not
                if name not in unique_list:
                    unique_list.append(name)
        # print list
        for name in unique_list:
            print('-', name)

    elif 'tags' in projectsOrTags:
        print('List of all distinct used tags:', sep='')
        for item in work:
            if 'end' and 'tags' in item:
                tags = item['tags']
                for tag in tags:
                    # check if exists in unique_list or not
                    if tag not in unique_list:
                        unique_list.append(tag)
        # print list
        for tags in unique_list:
            print('-', tags)
    else:
        print('Please enter \'projects\' or \'tags\' as arguments', sep='')





def print_elements(name):
    print(name,sep='')
