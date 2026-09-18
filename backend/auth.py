from fastapi import Header, HTTPException, Depends

# Extremely simple hackathon-ready RBAC
# In production, this would be a proper JWT validation against a user database.

ROLES = {
    "admin": 3,
    "operator": 2,
    "viewer": 1
}

async def get_current_role(x_role: str = Header(default="viewer", alias="X-Role")):
    role = x_role.lower()
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role specified.")
    return role

def require_role(min_role: str):
    async def role_checker(role: str = Depends(get_current_role)):
        if ROLES[role] < ROLES[min_role]:
            raise HTTPException(status_code=403, detail=f"Access denied. Minimum role required: {min_role}")
        return role
    return role_checker

require_admin = Depends(require_role("admin"))
require_operator = Depends(require_role("operator"))
require_viewer = Depends(require_role("viewer"))
