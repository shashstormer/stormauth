from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from authtuna import init_app
from authtuna.integrations import get_current_user_optional

app = FastAPI()

init_app(app)
app.add_middleware(CORSMiddleware, allow_origins=[
    "https://timeline.shashstorm.in"
], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/", tags=["Root"],)
async def root(user=Depends(get_current_user_optional)):
    """
    A public endpoint that anyone can access.
    """
    if user is None:
        return RedirectResponse("/auth/login")
    return RedirectResponse("/ui/dashboard")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5555, host="0.0.0.0", workers=2)
