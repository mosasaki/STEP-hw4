from absl import logging
import networkx as nx


def load_txt(file):
    """Open a test file and turn the contents into a list
    
    Args:
        file (str): The file location of the loading file
        
    Returns:
        A list of the file content
        
    Raises:
        IOError: An error occured accessing the file
    """

    try:
        with open(file) as in_file:
            loaded_list = in_file.readlines()
            return loaded_list
    except IOError as e:
        logging.fatal('Unable to open file %s' % file)


def create_graph(links_data):
    """Create a graph from the given list of links of users

    Args:
        links_data (list): A list of links between the users

    Return:
        graph (adjacency matrix): A graph of relations between the users
    """

    user_relations_graph = nx.DiGraph()

    for line in links_data:
        link_line = line.split(None)
        user_relations_graph.add_edge(link_line[0], link_line[1])

    return user_relations_graph


def create_user_dictionary(user_list):
    """Create a list of dictionary of username and number

     Args:
         user_list (list): A list of username and corresponding number

    Returns:
        user_data (list): A list of dictionary of username and number
     """
    users = []
    index = 0

    for user in user_list:
        user_line = user.split(None)
        user = {'index': user_line[0], 'name': user_line[1]}
        users.append(user)
        index += 1

    return users


def search_index_from_name(user_data, user_name):
    """Search index from input name

    Args:
        user_data(list): A list of dictionary of number and username
        user_name(str): An input username

    Returns:
        user[int] (int): The index of the user_name
    """

    index = 0

    for user in user_data:
        if user_name == user['name']:
            return user['index']
        index += 1

    print('Name does not exist')
    exit(1)


def add_count_steps(list):
    """
    Create a list of dictionary of index and step

    Args:
        list(list): An integer list
    return:
        count_step_added(list): A list of dictionary of index and step
    """

    count_step_added = []

    for i in list:
        i = {'index': i, 'step': 1}
        count_step_added.append(i)

    return count_step_added


def add_step(list, step):
    """
    Add steps

    Args:
        list(list): A list of dictionary of index and step
        step(int): An integer count of steps
    return:
        list(list): An updated version of list
    """

    for i in list:
        i['step'] += step

    return list


def search_steps(user_relations_graph, from_user, to_user, user_data):
    """search how many steps it'll take to find to_name from from_name

    Args:
        user_relations_graph(graph): A graph of users
        from_user(int): An index number of starting user
        to_user(int): An index number of goal user

    Returns:
        steps(int): An integer of the steps taken to find the to_user from from_user
    """

    queue = []
    step = 1
    already_checked = []

    try:
        queue.extend(list(user_relations_graph.succ[from_user]))
    except KeyError:
        print("The starting user does not follow anybody")
        step = 0

    queue = add_count_steps(queue)
    tmp_list = queue

    while queue != []:
        for node in tmp_list:
            if node['index'] == to_user:
                return node['step']

        tmp_list = []  # reset tmp_list

        tmp_list.extend(list(user_relations_graph.succ[queue[0]['index']]))

        tmp_index = 0
        tmp_list.insert(0, -1)  # insert dummy in head
        end_tmp_list = len(tmp_list)
        while tmp_index < end_tmp_list:  # exclude overlapping index
            for i in range(len(queue)):
                if tmp_list[tmp_index] == queue[i]['index']:
                    tmp_list.pop(tmp_index)
                    end_tmp_list -= 1
                    tmp_index -= 1

            tmp_index += 1
        tmp_list.pop(0)

        tmp_index = 0
        tmp_list.insert(0, -1)  # insert dummy in head
        end_tmp_list = len(tmp_list)
        while tmp_index < end_tmp_list:  # exclude overlapping index
            for i in range(len(already_checked)):
                if tmp_list[tmp_index] == already_checked[i]['index']:
                    tmp_list.pop(tmp_index)
                    end_tmp_list -= 1
                    tmp_index -= 1
            tmp_index += 1
        tmp_list.pop(0)

        tmp_list = add_count_steps(tmp_list)
        tmp_list = add_step(tmp_list, step)
        already_checked.append(queue[0])
        if queue[0]['step'] > step:
            step += 1
        queue.pop(0)
        queue.extend(tmp_list)

    print('It is impossible to reach the user by following the links')
    exit(1)


links_data = load_txt('links.txt')
graph = create_graph(links_data)
user_data = create_user_dictionary(load_txt('nicknames.txt'))


while True:
    print('from >')
    from_name = input().lower()
    from_index = search_index_from_name(user_data, from_name)
    print('to >')
    to_name = input().lower()
    to_index = search_index_from_name(user_data, to_name)
    steps = search_steps(graph, from_index, to_index, user_data)
    print("steps = %i" % steps)




