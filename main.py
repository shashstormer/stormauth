from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from authtuna import init_app, Theme, init_settings, ThemeMode, settings
from authtuna.integrations import get_current_user_optional
app = FastAPI()
new_theme = settings.THEME.dark.model_copy(deep=True)
new_theme.background_start = "#143497"
new_theme.background_end = "#000000"
custom_theme = Theme(
    mode="single", # only light mode vars but just set them to whatever you want they will be used in dark mode also.
    light=new_theme,
)

# Override settings with custom theme
init_settings(THEME=custom_theme, dont_use_env=False)
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
