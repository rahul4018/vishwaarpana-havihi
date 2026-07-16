from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    mobile: str | None
    role: str
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )