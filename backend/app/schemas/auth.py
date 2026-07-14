from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150,
        examples=["Rahul N"],
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["Rahul@123"],
    )

    mobile: str | None = Field(
        default=None,
        max_length=20,
        examples=["9876543210"],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class RegisterResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(
        from_attributes=True,
    )