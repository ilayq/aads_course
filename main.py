import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from maze import Maze 
from algo import solve, AlgoType


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/solve')
async def solve_maze(maze: Maze, algo: AlgoType) -> tuple[list[set[tuple[int, int]]], list[tuple[int, int]]]:
    return await solve(maze, algo)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, host='127.0.0.1', port=8000)

