import time
from jose import JWTError, jwt, ExpiredSignatureError
from OpenSSL import crypto
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import get_settings
from app.utils.logger import get_app_logger

logger = get_app_logger()
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
    logger.info("token is: %s", token)
    retries = 0
    while (retries < 3):
        try:
            jwt.decode(token, PUB_KEY, algorithms=[ALGORITHM])
            logger.info("Authorization was successful")
            return
        except ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except JWTError as exc:
            logger.error("JWT Verification Error: %s", exc)
            if "nbf" in str(exc):
                logger.error("Token not valid yet")
                logger.info("Waiting for token to become valid...")
                time.sleep(0.5)
                retries += 1
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from exc