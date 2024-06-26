from maze import Maze, Cell
from enum import Enum
from collections import deque
import math

import heapq


class AlgoType(Enum):
    bfs = 'bfs'
    greedy = 'greedy'
    a_star = 'a_star'


dirs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


async def bfs(maze: Maze) -> tuple[list[set[tuple[int, int]]], list[list[tuple[int, int]]]]:
    q: deque[tuple[int, int, int]] = deque() # i, j, step
    n, m = maze.height, maze.width
    steps: list[set[tuple[int, int]]] = [] 
    i, j = maze.start
    q.append((i, j, 0))
    visited: set[tuple[int, int]] = set()
    visited.add((i, j))
    path = [[0 for _ in range(maze.width)] for _ in range(maze.height)]
    path[i][j] = (i, j)
    while q:
        i, j, step = q.popleft()
        visited.add((i, j))

        if (i, j) == maze.end:
            return steps, path
        for di, dj in dirs:
            if -1 < i + di < n and -1 < j + dj < m and (i + di, j + dj) not in visited and maze.cells[i + di][j + dj]:
                q.append((i + di, j + dj, step + 1))
                visited.add((i + di, j + dj))
                path[i + di][j + dj] = (i, j)
        if q and q[0][2] > step:
            steps.append(visited.copy())
    for i in range(1, len(steps)):
        steps[i] = steps[i] - steps[i - 1]
    return steps, path
    

async def greedy(maze: Maze) -> tuple[list[set[tuple[int, int]]], list[list[tuple[int, int]]]]:
    heap: list[tuple[int, int, int]] = []
    n, m = maze.height, maze.width
    distance = lambda x1, y1, x2, y2: max(abs(x1 - x2), abs(y1 - y2))
    si, sj, ei, ey = (*maze.start, *maze.end)
    heapq.heappush(heap, (distance(si, sj, ei, ey), si, sj))
    visited: set[tuple[int, int]] = set()
    visited.add((si, sj))
    path = [[0 for _ in range(maze.width)] for _ in range(maze.height)]
    path[si][sj] = (si, sj)
    steps: list[set[tuple[int, int]]] = []
    while heap:
        _, i, j = heapq.heappop(heap) 
        visited.add((i, j))
        steps.append({(i, j)})
        if (i, j) == maze.end:
            return steps, path
        for di, dj in dirs:
            if -1 < i + di < n and -1 < j + dj < m and (i + di, j + dj) not in visited and maze.cells[i + di][j + dj]:
                visited.add((i + di, j + dj))
                heapq.heappush(heap, (distance(i + di, j + dj, ei, ey), i + di, j + dj))
                path[i + di][j + dj] = (i, j)
    return steps, path


async def a_star(maze: Maze) -> tuple[list[set[tuple[int, int]]], list[list[tuple[int, int]]]]:
    heap: list[tuple[int, int, int, int]] = []
    n, m = maze.height, maze.width
    si, sj, ei, ej = (*maze.start, *maze.end)
    distance = lambda step, i, j: step + max(abs(i - ei), abs(j - ej))
    heapq.heappush(heap, (distance(0, si, sj), 0, si, sj))
    visited: set[tuple[int, int]] = set()
    visited.add((si, sj))
    path = [[0 for _ in range(maze.width)] for _ in range(maze.height)]
    path[si][sj] = (si, sj)
    steps: list[set[tuple[int, int]]] = []
    while heap:
        _, step, i, j = heapq.heappop(heap)
        visited.add((i, j))
        steps.append(visited.copy())
        if (i, j) == maze.end:
            return steps, path
        for di, dj in dirs:
            if -1 < i + di < n and -1 < j + dj < m and (i + di, j + dj) not in visited and maze.cells[i + di][j + dj]:
                visited.add((i + di, j + dj))
                heapq.heappush(heap, (distance(step + 1, i + di, j + dj), step + 1, i + di, j + dj))
                path[i + di][j + dj] = (i, j)
    for i in range(1, len(steps)):
        steps[i] = steps[i] - steps[i - 1]
    return steps, path


async def solve(maze: Maze, algo: AlgoType) -> tuple[list[set[tuple[int, int]]], list[tuple[int, int]]]:
    result: list[set[tuple[int, int]]] = []
    if algo is AlgoType.bfs:
        result, path = await bfs(maze)
    elif algo is AlgoType.greedy:
        result, path = await greedy(maze)
    else:
        result, path = await a_star(maze)
    all_cells: set[tuple[int, int]] = set()
    for i in range(len(result)):
        result[i] -= all_cells
        all_cells |= result[i]
    i, j = maze.end
    total_path: list[tuple[int, int]] = []
    while path[i][j] != (i, j):
        total_path.append((i, j))
        i, j = path[i][j]        
    return [step for step in result if step], total_path[::-1] 


if __name__ == "__main__":
    import asyncio
    cells = [
                [1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 0, 1, 0, 0, 0, 1],
                [0, 1, 0, 1, 1, 1, 0, 1],
                [1, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 1, 1, 0, 1, 0, 1],
            ]
    for i in range(8):
        for j in range(8):
            cells[i][j] = Cell(cells[i][j])

    maze = Maze(
                width=8,
                height=8,
                cells=cells,
                start=(6, 0),
                end=(1, 7)
            )

    def print_res(res):
        for step in res:
            table = []
            for i in range(8):
                tmp = []
                for j in range(8):
                    if (i, j) in step:
                        tmp.append('^')
                    elif cells[i][j] is Cell.wall:
                        tmp.append('#')
                    else:
                        tmp.append('.')
                table.append(tmp)
            for row in table:
                print(*row)
            print('\n')

    res_bfs = asyncio.run(bfs(maze))
    print("BFS")
    print_res(res_bfs)

    print('\n\nGREEDY')
    print_res(asyncio.run(greedy(maze)))
    print('\n\nA*')
    print_res(asyncio.run(a_star(maze)))


