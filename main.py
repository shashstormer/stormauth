from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from authtuna import init_app, Theme, init_settings, ThemeMode, settings
from authtuna.integrations import get_current_user_optional, auth_service


@asynccontextmanager
async def lifecycle(app: FastAPI):
    # Other people if you want to allow anyone to create organizations you can
    # await auth_service.roles.add_permission_to_role("User", "org:create", "system")
    await auth_service.roles.get_or_create("OrgCreate", defaults={"description": "Users with this role can create organizations"})
    await auth_service.roles.add_permission_to_role("OrgCreate", "org:create", "system")
    await auth_service.roles.grant_relationship(granter_role_name="System", grantable_name="OrgCreate", grantable_manager=auth_service.roles, relationship_attr="can_assign_roles")
    user = await auth_service.users.get_by_email("shashanka5398@gmail.com")
    if user:
        await auth_service.roles.assign_to_user(user.id, "OrgCreate", "system", "global")
    yield

app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifecycle)
new_theme = settings.THEME.dark.model_copy(deep=True)
new_theme.background_start = "#152b72"
new_theme.background_end = "#081638"
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
