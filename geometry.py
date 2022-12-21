# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP3
"""

import math
import numpy as np
from alien import Alien
from typing import List, Tuple

def does_alien_touch_wall(alien, walls,granularity):
    """Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map

        Return:
            True if touched, False if not
    """

    def lte(x, y):
        return x <= y or np.isclose(x, y)
    if alien.is_circle():
        for wall in walls:
            radial_distance = point_segment_distance(alien.get_centroid(), ((wall[0], wall[1]), (wall[2], wall[3])))
            if lte(radial_distance, alien.get_width() + (granularity/math.sqrt(2))):
                return True
    else:
        co_ord = alien.get_head_and_tail()
        for wall in walls:
            distance = segment_distance((co_ord[0], co_ord[1]), ((wall[0], wall[1]), (wall[2], wall[3])))
            if distance == 0 and lte(distance, (alien.get_width() + granularity / math.sqrt(2))):
                return True
            radial_distance = point_segment_distance(alien.get_centroid(), ((wall[0], wall[1]), (wall[2], wall[3])))
            if lte(radial_distance, (alien.get_width()*1.5 + (granularity / math.sqrt(2)))):
                return True
    return False

def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """

    def circle(x1, y1, r1, x2, y2, r2):
        d = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
        return lte(d, r1 + r2)

    def lte(x, y):
        return x <= y or np.isclose(x, y)

    if alien.is_circle():
        for wall in goals:
            alien_center = alien.get_centroid()
            if circle(alien_center[0], alien_center[1], alien.get_width(), wall[0], wall[1], wall[2]):
                return True
    else:
        co_ord = alien.get_head_and_tail()
        for wall in goals:
            radial_distance = point_segment_distance((wall[0], wall[1]), co_ord)
            if lte(radial_distance, (alien.get_width() + wall[2])):
                return True
    return False

def is_alien_within_window(alien, window, granularity):
    """Determine whether the alien stays within the window

        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """
    granularity = granularity/math.sqrt(2)
    def window_compare_x(val):
        return 0 >= val or val >= window[0]

    def window_compare_y(val):
        return 0 >= val or val >= window[1]

    if alien.is_circle():
        position = alien.get_centroid()
        if window_compare_x(position[0] + alien.get_width() + granularity) or window_compare_x(position[0] - alien.get_width() - granularity) or window_compare_y(position[1] + alien.get_width() + granularity) or window_compare_y(position[1] - alien.get_width() - granularity):
            return False
    else:
        co_ord = alien.get_head_and_tail()
        if window_compare_x(co_ord[0][0] + alien.get_width() + granularity) or window_compare_x(co_ord[0][0] - alien.get_width() - granularity) or window_compare_y(co_ord[0][1] - alien.get_width() - granularity) or window_compare_y(co_ord[0][1] + alien.get_width() + granularity) or window_compare_x(co_ord[1][0] + alien.get_width() + granularity) or window_compare_x(co_ord[1][0] - alien.get_width() - granularity) or window_compare_y(co_ord[1][1] - alien.get_width() - granularity) or window_compare_y(co_ord[1][1] + alien.get_width() + granularity):
            return False

    return True

def point_segment_distance(point, segment):
    """Compute the distance from the point to the line segment.
    Hint: Lecture note "geometry cheat sheet"

        Args:
            point: A tuple (x, y) of the coordinates of the point.
            segment: A tuple ((x1, y1), (x2, y2)) of coordinates indicating the endpoints of the segment.

        Return:
            Euclidean distance from the point to the line segment.
    """
    # unit vector
    segment = np.array(segment)
    unit_line = segment[1] - segment[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)

    # compute the perpendicular distance to the theoretical infinite line
    segment_dist = (
            np.linalg.norm(np.cross(segment[1] - segment[0], segment[0] - point)) /
            np.linalg.norm(unit_line)
    )

    diff = (
            (norm_unit_line[0] * (point[0] - segment[0][0])) +
            (norm_unit_line[1] * (point[1] - segment[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + segment[0][0]
    y_seg = (norm_unit_line[1] * diff) + segment[0][1]

    endpoint_dist = min(
        np.linalg.norm(segment[0] - point),
        np.linalg.norm(segment[1] - point)
    )

    # decide if the intersection point falls on the line segment
    lp1_x = segment[0][0]  # line point 1 x
    lp1_y = segment[0][1]  # line point 1 y
    lp2_x = segment[1][0]  # line point 2 x
    lp2_y = segment[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        return endpoint_dist

def do_segments_intersect(segment1, segment2):
    """Determine whether segment1 intersects segment2.  
    We recommend implementing the above first, and drawing down and considering some examples.
    Lecture note "geometry cheat sheet" may also be handy.

        Args:
            segment1: A tuple of coordinates indicating the endpoints of segment1.
            segment2: A tuple of coordinates indicating the endpoints of segment2.

        Return:
            True if line segments intersect, False if not.
    """
    # Reference source : https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    def onSegment(p, q, r):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    def orientation(p, q, r):
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):

            # Clockwise orientation
            return 1
        elif (val < 0):

            # Counterclockwise orientation
            return 2
        else:

            # Collinear orientation
            return 0

    o1 = orientation(segment1[0], segment1[1], segment2[0])
    o2 = orientation(segment1[0], segment1[1], segment2[1])
    o3 = orientation(segment2[0], segment2[1], segment1[0])
    o4 = orientation(segment2[0], segment2[1], segment1[1])

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(segment1[0], segment2[0], segment1[1])):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(segment1[0], segment2[1], segment1[1])):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(segment2[0], segment1[0], segment2[1])):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(segment2[0], segment1[1], segment2[1])):
        return True

    # If none of the cases
    return False

def segment_distance(segment1, segment2):
    """Compute the distance from segment1 to segment2.  You will need `do_segments_intersect`.
    Hint: Distance of two line segments is the distance between the closest pair of points on both.

        Args:
            segment1: A tuple of coordinates indicating the endpoints of segment1.
            segment2: A tuple of coordinates indicating the endpoints of segment2.

        Return:
            Euclidean distance between the two line segments.
    """
    if do_segments_intersect(segment1, segment2):
        return 0
    # try each of the 4 vertices w/the other segment
    distances = []
    distances.append(point_segment_distance(segment1[0], segment2))
    distances.append(point_segment_distance(segment1[1], segment2))
    distances.append(point_segment_distance(segment2[0], segment1))
    distances.append(point_segment_distance(segment2[1], segment1))
    return min(distances)

if __name__ == '__main__':

    from geometry_test_data import walls, goals, window, alien_positions, alien_ball_truths, alien_horz_truths, \
        alien_vert_truths, point_segment_distance_result, segment_distance_result, is_intersect_result

    # Here we first test your basic geometry implementation
    def test_point_segment_distance(points, segments, results):
        num_points = len(points)
        num_segments = len(segments)
        for i in range(num_points):
            p = points[i]
            for j in range(num_segments):
                seg = ((segments[j][0], segments[j][1]), (segments[j][2], segments[j][3]))
                cur_dist = point_segment_distance(p, seg)
                assert abs(cur_dist - results[i][j]) <= 10 ** -3, \
                    f'Expected distance between {points[i]} and segment {segments[j]} is {results[i][j]}, ' \
                    f'but get {cur_dist}'

    def test_do_segments_intersect(center: List[Tuple[int]], segments: List[Tuple[int]],
                                   result: List[List[List[bool]]]):
        for i in range(len(center)):
            for j, s in enumerate([(40, 0), (0, 40), (100, 0), (0, 100), (0, 120), (120, 0)]):
                for k in range(len(segments)):
                    cx, cy = center[i]
                    st = (cx + s[0], cy + s[1])
                    ed = (cx - s[0], cy - s[1])
                    a = (st, ed)
                    b = ((segments[k][0], segments[k][1]), (segments[k][2], segments[k][3]))
                    if do_segments_intersect(a, b) != result[i][j][k]:
                        if result[i][j][k]:
                            assert False, f'Intersection Expected between {a} and {b}.'
                        if not result[i][j][k]:
                            assert False, f'Intersection not expected between {a} and {b}.'


    def test_segment_distance(center: List[Tuple[int]], segments: List[Tuple[int]], result: List[List[float]]):
        for i in range(len(center)):
            for j, s in enumerate([(40, 0), (0, 40), (100, 0), (0, 100), (0, 120), (120, 0)]):
                for k in range(len(segments)):
                    cx, cy = center[i]
                    st = (cx + s[0], cy + s[1])
                    ed = (cx - s[0], cy - s[1])
                    a = (st, ed)
                    b = ((segments[k][0], segments[k][1]), (segments[k][2], segments[k][3]))
                    distance = segment_distance(a, b)
                    assert abs(result[i][j][k] - distance) <= 10 ** -3, f'The distance between segment {a} and ' \
                                                                  f'{b} is expected to be {result[i]}, but your' \
                                                                  f'result is {distance}'

    def test_helper(alien: Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()

        touch_wall_result = does_alien_touch_wall(alien, walls, 0)
        touch_goal_result = does_alien_touch_goal(alien, goals)
        in_window_result = is_alien_within_window(alien, window, 0)

        assert touch_wall_result == truths[
            0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, ' \
                f'expected: {truths[0]}'
        assert touch_goal_result == truths[
            1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, ' \
                f'expected: {truths[1]}'
        print("success")
        assert in_window_result == truths[
            2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, ' \
                f'expected: {truths[2]}'


    # Initialize Aliens and perform simple sanity check.
    alien_ball = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Ball', window)
    test_helper(alien_ball, alien_ball.get_centroid(), (False, False, True))

    alien_horz = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal', window)
    test_helper(alien_horz, alien_horz.get_centroid(), (False, False, True))

    alien_vert = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical', window)
    test_helper(alien_vert, alien_vert.get_centroid(), (True, False, True))

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal',
                            window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical',
                            window)

    centers = alien_positions
    segments = walls
    test_point_segment_distance(centers, segments, point_segment_distance_result)
    test_do_segments_intersect(centers, segments, is_intersect_result)
    test_segment_distance(centers, segments, segment_distance_result)

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    # Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110, 55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))

    print("Geometry tests passed\n")