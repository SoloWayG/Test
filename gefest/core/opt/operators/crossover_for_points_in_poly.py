import copy
import random
from multiprocessing import Pool
import numpy as np
from numpy.linalg import norm
from gefest.core.algs.postproc.resolve_errors import postprocess
from gefest.core.opt.constraints import check_constraints
from gefest.core.structure.domain import Domain
from gefest.core.structure.point import Point
from gefest.core.structure.polygon import Polygon
from gefest.core.structure.structure import Structure

MAX_ITER = 50000
NUM_PROC = 1


def crossover_worker(args):
    """
    That crossover take two polygons (structures with only 1 poly), then points of polys placed to common point cloud.
    Then, from this cloud crossover will create a new poly, that will consist of previous polygons.
    In idea, this crossover must creat intermediate polygon, from 2 paretns polys
    """

    s1, s2, domain = args[0], args[1], args[2]
    geometry = domain.geometry
    poly_sum = (len(s1.polygons[0].points)+len(s2.polygons[0].points))//2     #set size (count of points) of new poly
    poly_lenght = random.randint(domain.min_points_num, poly_sum)            #random choose count of points

    points_for_crossovering = [i.coords()[:2] for i in s1.polygons[0].points[:-1]] #take points from first poly as a coords. Without last point
    for i in [i.coords()[:2] for i in s2.polygons[0].points[:-1]]:
        if i not in points_for_crossovering:
            points_for_crossovering.append(i)                                       #Adding points from second polygon, if that points not in firts poly
    new_poly_points =[]                                                              #init child poly
    dist_between_poitns = domain.dist_between_points                                #init min distance between point< to validate poly side size
    new_structure = copy.deepcopy(points_for_crossovering)
    trys=0
    while len(new_poly_points) < poly_lenght:
        trys+=1
        if trys==(poly_lenght**2)*2:
            return s1
        '''
        random choosing point, from polygons points 
        then append them to new_poly_points
        '''
        rndchoice = random.choice(points_for_crossovering)
        if rndchoice not in new_poly_points:
            new_poly_points.append(rndchoice)
        ind = len(new_poly_points) - 1
        if ind > 0:                     #starting from second point, we cheking distance between i-1 and i points
            if norm(np.array(new_poly_points[ind]) - np.array(new_poly_points[ind - 1]), ord=1) < dist_between_poitns:
                del new_poly_points[ind]    # if distance is too short - delete that point from child poly
        if len(new_poly_points) == poly_lenght: #check distance between last and first points. It need to close poly
            if norm(np.array(new_poly_points[-1]) - np.array(new_poly_points[0]), ord=1) < dist_between_poitns:
                del new_poly_points[-1]
        if len(new_poly_points) == poly_lenght and domain.is_closed:
            new_poly_points.append(new_poly_points[0])

    points_ = [Point(i[0], i[1]) for i in new_poly_points]
    #poly = geometry.get_convex(Polygon('tmp', points=points_))  # avoid self intersection in polygon
    #points_ = poly.points


    polygon_crossered = Polygon('Crossovered', points=points_)


    #crossover_point = random.randint(1, len(new_structure.polygons) + 1)  # Choosing crossover point randomly
    #
    # # Crossover conversion
    # part_1 = s1.polygons[0:crossover_point]
    # if not isinstance(part_1, list):
    #     part_1 = [part_1]
    # part_2 = s2.polygons[crossover_point:len(s1.polygons)]
    # if not isinstance(part_2, list):
    #     part_2 = [part_2]
    #
    # result = copy.deepcopy(part_1)
    # result.extend(copy.deepcopy(part_2))
    new_structure = Structure(polygons=[polygon_crossered])
    #new_structure.polygons = polygon_crossered

    # Postprocessing for new structure
    new_structure = postprocess(new_structure, domain)
    constraints = check_constraints(structure=new_structure, domain=domain)
    max_attempts = 3  # Number of postprocessing attempts
    while not constraints:
        new_structure = postprocess(new_structure, domain)
        constraints = check_constraints(structure=new_structure, domain=domain)
        max_attempts -= 1
        if max_attempts == 0:
            # If the number of attempts is over,
            # the transformation is considered unsuccessful
            # and one of the structures is returned
            return s1
    return new_structure


def crossover(s1: Structure, s2: Structure, domain: Domain, rate=0.4):
    random_val = random.random()
    if random_val >= rate:# or len(s1.polygons) == 1 or len(s2.polygons) == 1:

        return s1
    if len(s1.polygons) == 0:
        return s2
    elif len(s2.polygons) == 0:
        return s1

    new_structure = s1

    if NUM_PROC > 1:
        # Calculations on different processor cores
        with Pool(NUM_PROC) as p:
            new_items = p.map(crossover_worker,
                              [[s1, s2, domain] for _ in range(NUM_PROC)])
    else:
        new_items = [crossover_worker([s1, s2, domain]) for _ in range(NUM_PROC)]

    for structure in new_items:
        if structure is not None:
            new_structure = structure
            break

    return new_structure
