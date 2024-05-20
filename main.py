import fastapi
import uvicorn

from maze import Maze 
from algo import solve, AlgoType


app = fastapi.FastAPI()


@app.post('/solve')
async def solve_maze(maze: Maze, algo: AlgoType) -> list[set[tuple[int, int]]]:
    return await solve(maze, algo)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)

