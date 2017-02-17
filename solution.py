""" This is a solution to the HouseCanary Paper Streets coding challenge (http://bit.ly/2d9Ee8g). """


def count_paper_streets(x_intercepts: list, y_intercepts: list, homes: list) -> int:
    """ Finds the number of groups of paper streets on the map represented by the given x & y intercepts and homes
    A street is a line segment that starts and ends at intersections. A street is a paper street if it has no
    homes on it (a home on either of the endpoints of the street doesn't count). A group is made of paper streets
    that all share at least one point with one other paper street in that group.
    Args:
        x_intercepts (list):
            a list of ints representing the x intercepts of the vertical lines of the map
        y_intercepts (list):
            a list of ints representing the y intercepts of the horizontal lines of the map
        homes (list):
            a list of tuples representing the x, y coordinates of all the homes on the map
    Returns:
        the count of the groups of paper streets on the map
    """
    homes = __get_homes_not_on_intersections(x_intercepts, y_intercepts, homes)
    paper_streets = [street for street in __generate_streets(x_intercepts, y_intercepts) if street.isdisjoint(homes)]
    paper_groups = __group_streets(paper_streets)
    return len(paper_groups)


def __get_homes_not_on_intersections(x_intercepts: list, y_intercepts: list, homes: list) -> set:
    """ Returns a set of the given homes whose coordinates are not in the given x & y intercepts
    This helper method reduces the number of homes to consider when determining if a street is a paper street by
    removing homes on intersections.
    Args:
        x_intercepts (list):
            a list of ints representing the x intercepts of the vertical lines of the map
        y_intercepts (list):
            a list of ints representing the y intercepts of the horizontal lines of the map
        homes (list):
            a list of tuples representing the x, y coordinates of all the homes on the map
    Returns:
        a set of tuples representing the x, y  coordinates of all the homes on the map that aren't on the
        intersection of two roads
    """
    return {(x, y) for x, y in homes if x not in x_intercepts or y not in y_intercepts}


def __generate_streets(x_intercepts: list, y_intercepts: list) -> set:
    """ A generator that yields all the line segments defined by the given x_intercepts and y_intercepts
    Args:
        x_intercepts (list):
            a list of ints representing the x intercepts of the vertical lines of the map
        y_intercepts (list):
            a list of ints representing the y intercepts of the horizontal lines of the map
    Yields:
        a set of all the points on the line segment, represented as tuples, including the endpoints of the segment for
        all the horizontal and vertical line segments of the grid defined by the given x_intercepts and y_intercepts.
    """
    for x_start, x_end in zip(x_intercepts[:-1], x_intercepts[1:]):
        for y in y_intercepts:
            yield {(x, y) for x in range(x_start, x_end + 1)}
    for y_start, y_end in zip(y_intercepts[:-1], y_intercepts[1:]):
        for x in x_intercepts:
            yield {(x, y) for y in range(y_start, y_end + 1)}


def __group_streets(streets: list) -> list:
    """ Combines the given streets into groups such that no group intersects another group
    This method uses recursion to ensure that the returned groups don't have any intersections.
    Args:
        streets (list):
            a list of sets of tuples where the sets represent streets and the tuples contain coordinates on the street
    Returns:
        a list of sets of tuples that represent all the groups of streets that can be formed from the given streets.
        A group is made up of streets that all share at least one point with another street in the group
    """
    groups = []
    for street in streets:
        for group in groups:
            if not street.isdisjoint(group):
                group.update(street)
                break
        else:
            groups.append(street)
    return groups if len(groups) == len(streets) else __group_streets(groups)
