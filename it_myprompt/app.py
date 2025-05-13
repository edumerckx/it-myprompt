from fastapi import FastAPI

from it_myprompt.routes.auth import router as auth_router
from it_myprompt.routes.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)


@app.get('/')
async def root():
    return {'message': 'it-myprompt'}
