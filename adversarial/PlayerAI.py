#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 12:01:39 2017

@author: georgos
"""

from BaseAI_3 import BaseAI

# from Grid_3 import Grid
import time
import math


class PlayerAI(BaseAI):
    def getMove(self, grid):

        start = time.clock()
        t = 2
        res = []
        while time.clock() - start < 0.098:
            alpha = -10000
            beta = 10000
            minMax = MiniMax(grid, start, t)
            child, temp = minMax.maximize(grid, alpha, beta)
            res.append([t, child])
            t += 2
        return res[-2][1]


class MiniMax:
    def __init__(self, grid, start, t):

        self.count = 0
        self.t = t
        self.start = start
        self.f = {"path": "0", "parent": "1"}
        self.NODES = {}
        self.NODES[str(grid.map)] = {self.f["path"]: "", self.f["parent"]: ""}

    def buildNode(self, parent, child, s):

        self.NODES[child] = {self.f["path"]: "", self.f["parent"]: parent}
        self.NODES[child][self.f["path"]] = self.NODES[parent][self.f["path"]] + s

        return self.NODES

    def maximize(self, grid, alpha, beta):

        self.count += 1

        if grid.canMove() == False or len(self.NODES[str(grid.map)][self.f["path"]]) >= self.t:

            heur = Heuristic()
            utility = heur.compute(grid)
            return tuple((None, utility))

        maxChild, maxUtility = tuple((None, -10000))

        directions = grid.getAvailableMoves()

        for d in directions:
            if time.clock() - self.start > 0.098:
                break

            grid_copy = grid.clone()
            grid_copy.move(d)

            parent = str(grid.map)
            child = str(grid_copy.map)
            self.buildNode(parent, child, str(d))

            _, utility = self.minimize(grid_copy, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility = tuple((d, utility))

            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return tuple((maxChild, maxUtility))

    def minimize(self, grid, alpha, beta):

        self.count += 1

        if grid.canMove() == False or len(self.NODES[str(grid.map)][self.f["path"]]) >= self.t - 1:

            heur = Heuristic()
            utility = heur.compute(grid)
            return tuple((None, utility))

        minChild, minUtility = tuple((None, 10000))

        positions = grid.getAvailableCells()

        for p in positions:
            for n in [2, 4]:
                if time.clock() - self.start > 0.098:
                    break

                grid_copy = grid.clone()
                grid_copy.insertTile(p, n)

                parent = str(grid.map)
                child = str(grid_copy.map)
                self.buildNode(parent, child, str(p))

                _, utility = self.maximize(grid_copy, alpha, beta)

                if utility < minUtility:
                    minChild, minUtility = tuple((p, utility))

                if minUtility <= alpha:
                    break
                if minUtility < beta:
                    beta = minUtility

        return tuple((minChild, minUtility))

    def getCount(self):
        return self.count

    def getNodes(self):
        return self.NODES


class Heuristic:
    def __init__(self, size=4):
        self.size = size

    def compute(self, grid):

        heu1 = self.heuristicMonotonicity(grid)
        heu2 = self.heuristicMerge(grid)
        heu3 = self.heuristicAngle(grid)

        if grid.getMaxTile() > 1000:
            heu = heu1 + heu2 * 0.8 + heu3 * 1.4 + len(grid.getAvailableCells()) * (grid.getMaxTile() // 10)
        else:
            heu = heu1 + heu2 + heu3 + len(grid.getAvailableCells()) * (grid.getMaxTile() // 50)

        return heu

    def heuristicMonotonicity(self, grid):
        heuMono = 0
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                if grid.getCellValue([i, j]) > grid.getCellValue([i, j + 1]):
                    heuMono += grid.getCellValue([i, j]) // 3
                elif grid.getCellValue([i, j]) > grid.getCellValue([i + 1, j]):
                    heuMono += grid.getCellValue([i, j]) // 3
                elif grid.getCellValue([i, j]) > grid.getCellValue([i + 1, j + 1]):
                    heuMono += grid.getCellValue([i, j]) // 3
        return heuMono

    def heuristicMerge(self, grid):
        heuMerge = 0
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                if grid.getCellValue([i, j]) == grid.getCellValue([i, j + 1]):
                    heuMerge += grid.getCellValue([i, j]) // 2
                elif grid.getCellValue([i, j]) == grid.getCellValue([i + 1, j]):
                    heuMerge += grid.getCellValue([i, j]) // 2
        return heuMerge

    def heuristicAngle(self, grid):

        if grid.getMaxTile() > 1000:
            part1 = 4 * grid.getCellValue([0, 0])
        else:
            part1 = 6 * grid.getCellValue([0, 0])
        part2 = 3 * grid.getCellValue([0, 1]) + 3 * grid.getCellValue([1, 0])
        part3 = 2 * grid.getCellValue([0, 2]) + 2 * grid.getCellValue([2, 0])

        heuAngle = part1 + part2 + part3

        return heuAngle
