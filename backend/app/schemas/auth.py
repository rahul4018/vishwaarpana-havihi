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


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["Rahul@123"],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    user: RegisterResponse
    tokens: TokenResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        min_length=1,
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"