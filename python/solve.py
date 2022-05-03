"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from file_wrappers import StdinFileWrapper, StdoutFileWrapper

from point import Point

import random

def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    )

def solve_simple_greedy(instance: Instance) -> Solution:
    towers_list = []

    cityset = set(instance.cities)
    deadcities = set()
    #build towers_list
    while len(cityset) > 0:
        best_point = Point(x=0, y=0)
        max_overlap = 0
        for i in range(instance.grid_side_length):
            for j in range(instance.grid_side_length):
                #check how many cities this overlaps
                if (i, j) in deadcities:
                    continue
                temp = Point(x=i, y=j)
                count = 0
                for city in cityset:
                    if temp.distance_sq(city) <= instance.coverage_radius**2:
                        count += 1
                #update best tower
                if count >= max_overlap:
                    best_point = temp
                    max_overlap = count
                elif count == 0:
                    deadcities.add((i, j))

        
        #place tower down         
        towers_list.append(best_point)
        #mark all cities touching tower as "covered"
        setcopy = cityset.copy()
        for city in cityset:
            if best_point.distance_sq(city) <= instance.coverage_radius**2:
                setcopy.remove(city)
        cityset = setcopy

    return Solution(instance=instance, towers=towers_list)

def solve_forreal(instance: Instance) -> Solution:
    towers_list = []

    cityset = set(instance.cities)
    deadcities = set()
    #build towers_list
    while len(cityset) > 0:
        
        max_overlap = 0
        best_towers = set()
        for i in range(instance.grid_side_length):
            for j in range(instance.grid_side_length):
                #check how many cities this overlaps
                if (i, j) in deadcities:
                    continue
                temp = Point(x=i, y=j)
                count = 0
                for city in cityset:
                    if temp.distance_sq(city) <= instance.coverage_radius**2:
                        count += 1
                #update best tower
                if count > max_overlap:
                    best_towers = set()
                    best_towers.add(temp)
                    max_overlap = count
                elif count == max_overlap:
                    best_towers.add(temp)
                elif count == 0:
                    deadcities.add((i, j))

        #select best point out of all the best tower candidates
        best_point = Point(x=0, y=0)
        min_overlap = float('inf')
        for candidate in best_towers:
            count = 0
            for tower in towers_list:
                if candidate.distance_sq(tower) <= instance.penalty_radius**2:
                    count += 1
            if count <= min_overlap:
                best_point = candidate
                min_overlap = count

        #place tower down         
        towers_list.append(best_point)
        #mark all cities touching tower as "covered"
        setcopy = cityset.copy()
        for city in cityset:
            if best_point.distance_sq(city) <= instance.coverage_radius**2:
                setcopy.remove(city)
        cityset = setcopy

    return Solution(instance=instance, towers=towers_list)

def solve_minnie(instance: Instance) -> Solution:
    towers_list = []

    cityset = set(instance.cities)
    deadcities = set()
    #build towers_list
    while len(cityset) > 0:
        
        max_overlap = 0
        best_towers = set()
        for i in range(instance.grid_side_length):
            for j in range(instance.grid_side_length):
                #check how many cities this overlaps
                if (i, j) in deadcities:
                    continue
                temp = Point(x=i, y=j)
                count = 0
                for city in cityset:
                    if temp.distance_sq(city) <= instance.coverage_radius**2:
                        count += 1
                #update best tower
                if count > max_overlap:
                    best_towers = set()
                    best_towers.add(temp)
                    max_overlap = count
                elif count == max_overlap:
                    best_towers.add(temp)
                elif count == 0:
                    deadcities.add((i, j))

        #select best point out of all the best tower candidates
        best_points = []
        min_overlap = float('inf')
        for candidate in best_towers:
            count = 0
            for tower in towers_list:
                if candidate.distance_sq(tower) <= instance.penalty_radius**2:
                    count += 1
            if count < min_overlap:
                best_points = [candidate]
                min_overlap = count
            elif count == min_overlap:
                best_points.append(candidate)
        
        best_point = random.choice(best_points)

        #place tower down         
        towers_list.append(best_point)
        #mark all cities touching tower as "covered"
        setcopy = cityset.copy()
        for city in cityset:
            if best_point.distance_sq(city) <= instance.coverage_radius**2:
                setcopy.remove(city)
        cityset = setcopy

    return Solution(instance=instance, towers=towers_list)


SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive,
    "forreal": solve_forreal
}


# You shouldn't need to modify anything below this line.
def infile(args):
    if args.input == "-":
        return StdinFileWrapper()

    return Path(args.input).open("r")


def outfile(args):
    if args.output == "-":
        return StdoutFileWrapper()

    return Path(args.output).open("w")


def main(args):
    with infile(args) as f:
        instance = Instance.parse(f.readlines())
        solver = SOLVERS[args.solver]
        solution = solver(instance)
        assert solution.valid()
        with outfile(args) as g:
            print("# Penalty: ", solution.penalty(), file=g)
            solution.serialize(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem instance.")
    parser.add_argument("input", type=str, help="The input instance file to "
                        "read an instance from. Use - for stdin.")
    parser.add_argument("--solver", required=True, type=str,
                        help="The solver type.", choices=SOLVERS.keys())
    parser.add_argument("output", type=str,
                        help="The output file. Use - for stdout.",
                        default="-")
    main(parser.parse_args())
