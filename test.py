import os

from authtuna.integrations.fastapi_integration import auth_service
async def add_missing_user_role():
    """
    I added the User role some versions before, but i had deployed before that version so this function allows people to migrate from an older version to newer version.
    """
    users = await auth_service.users.list(limit=100)
    for user in users:
        print(user)
    print("-" * 50)
    users_roled = await auth_service.roles.get_users_for_role("User")
    roled_unames = []
    for user in users_roled:
        if user["scope"] == "global":
            roled_unames.append(user["username"])
    for user in users:
        if user.username not in roled_unames and user.username != "system":
            await auth_service.roles.assign_to_user(user.id, "User", "system", 'global')
            print("Added user role to : ", user.username)

async def give_superadmin():
    me = await auth_service.users.get_by_email(os.getenv("EMAIL_FOR_SUPERADMIN"))
    await auth_service.roles.assign_to_user(me.id, "SuperAdmin", "system", "global")

async def main():
    await add_missing_user_role()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())