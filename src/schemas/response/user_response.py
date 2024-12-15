from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    hashed_password: str
    is_active: bool
    is_team_lead: bool

    class Config:
        orm_mode = True
        from_attributes = True
