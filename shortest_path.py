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
        print('Unable to open file %s' % file)
        exit(1)


def create_graph(links_data):
    """Create a graph from the given list of links of pages

    Args:
        links_data (list): A list of links between the pages

    Return:
        graph (adjacency matrix): A graph of relations between the pages
    """

    pages_relations_graph = nx.DiGraph()

    for line in links_data:
        link_line = line.split(None)
        pages_relations_graph.add_edge(link_line[0], link_line[1])

    return pages_relations_graph


def add_attributes_to_graph(graph, page_dic_list):
    """Add attributes to a graph

    Args:
        graph (graph): A graph of users
        page_dic_list (list): A list of dictionary of username and number

    Return:
        graph (adjacency matrix): A graph with attributes
    """

    for line in list(graph.nodes):
        graph.nodes[line]['page'] = page_dic_list[int(line)]['page']

    return graph


def create_user_dictionary(pages_list):
    """Create a list of dictionary of page and index

     Args:
         user_list (list): A list of pages and corresponding index

    Returns:
        user_data (list): A list of dictionary of page and index
     """
    pages = []
    index = 0

    for page in pages_list:
        page_line = page.split(None)
        page = {'index': page_line[0], 'page': page_line[1]}
        pages.append(page)
        index += 1

    return pages


def search_index_from_name(page_data, page_name):
    """Search index from input page

    Args:
        page_data(list): A list of dictionary of page and index
        page_name(str): An input page

    Returns:
        user[int] (int): The index of the page
    """

    index = 0

    for page in page_data:
        if page_name == page['page']:
            return page['index']
        index += 1

    print('Page does not exist')
    exit(1)


def search_shortest_paths(graph, from_link, to_link):
    """
    Search and retrun the shortest path between two pages

    Args:
        graph(graph): A graph of pages
        from_link(int): An index number of starting page
        to_link(int): An index number of goal page

    Returns:
        path_list(list): A list of path
    """

    path_list =[]
    try:
        path_key_list = nx.shortest_path(graph, source=from_link, target=to_link)
    except nx.exception.NetworkXNoPath:
        return 'no path between the two pages'

    index = 0

    while index < len(path_key_list):
        for key in graph.nodes:
            if key == path_key_list[index]:
                path_list.append(graph.nodes[key]['page'])
        index += 1

    return path_list


links_data = load_txt('wikipedia_links/links.txt')
pages_data = create_user_dictionary(load_txt('wikipedia_links/pages.txt'))
graph = create_graph(links_data)
graph = add_attributes_to_graph(create_graph(links_data), pages_data)

while True:
    print('from >')
    from_page = input().lower()
    from_index = search_index_from_name(pages_data, from_page)
    print('to >')
    to_page = input().lower()
    to_index = search_index_from_name(pages_data, to_page)
    path = search_shortest_paths(graph, from_index, to_index)
    steps = len(path) - 1
    print("steps taken: %i" % steps)
    print("path: ", end = '')
    print(path)
