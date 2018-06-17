import numpy as np

__all__ = ['segment_intersect', 'point_is_near_point', 'point_is_on_line', 'is_collinear']


def determine_slope(p1, p2):
    """Determines the slope of a line

    :param p1:
    :param p2:
    :return:
    """
    return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])


def y_intercept(slope, p1):
    """Determines the y value of the intersection with the y axis.

    :param slope:
    :param p1:
    :return:
    """
    return p1[1] - 1. * slope * p1[0]


def intersect(line1, line2):
    """Determines the intersection of two lines.

    :param line1:
    :param line2:
    :return:
    """
    min_allowed = 1e-5  # guard against overflow
    big_value = 1e10  # use instead (if overflow would have occurred)
    m1 = determine_slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])
    m2 = determine_slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])
    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x, y


def segment_intersect(line1, line2):
    """Returns the point of intersection if it exists else it returns None.

    :param line1:
    :param line2:
    :return:
    """
    intersection_pt = intersect(line1, line2)

    print(line1[0][0], line1[1][0], line2[0][0], line2[1][0], intersection_pt[0])
    print(line1[0][1], line1[1][1], line2[0][1], line2[1][1], intersection_pt[1])

    if line1[0][0] < line1[1][0]:
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            print('exit 1')
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            print('exit 2')
            return None

    if line2[0][0] < line2[1][0]:
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            print('exit 3')
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            print('exit 4')
            return None

    return intersection_pt


def point_is_near_point(point_0, point_1, error=0.001):
    """Return true iff the two points are near each other.

    :param point_0:
    :param point_1:
    :param error:
    :return:
    """
    return np.linalg.norm(point_0 - point_1) < error


def point_is_on_line(point, line_start, line_end, error=0.001):
    """Return true iff the point intersects the line.

    :param point:
    :param line_start:
    :param line_end:
    :param error:
    :return:
    """
    # We take the wedge- and dot product to determine if the point intersects the line
    v = line_end - point
    w = point - line_start
    return np.linalg.det(np.column_stack((v, w))) < error and np.dot(v, w) > 0


def is_collinear(point_0, point_1, point_2, error=0.001):
    """Return true iff the three points are collinear

    :param point_0:
    :param point_1:
    :param point_2:
    :param error:
    :return:
    """
    # We take the wedge product to determine if the three points are collinear
    v = point_2 - point_1
    w = point_0 - point_1
    return np.linalg.det(np.column_stack((v, w))) < error
