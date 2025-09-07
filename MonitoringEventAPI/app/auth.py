from jose import JWTError, jwt, ExpiredSignatureError
from OpenSSL import crypto
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import get_settings

settings = get_settings()

PUB_KEY_PATH = settings.PUB_KEY_PATH
ALGORITHM = settings.ALGORITHM

def _get_public_key(filepath: str) -> bytes:
    with open(filepath, "rb") as cert_file:
        cert = cert_file.read()

    crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    pubKeyObject = crtObj.get_pubkey()
    return crypto.dump_publickey(crypto.FILETYPE_PEM, pubKeyObject)

security = HTTPBearer()

PUB_KEY = _get_public_key(PUB_KEY_PATH)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> None:
    token = credentials.credentials
    try:
        jwt.decode(token, PUB_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
