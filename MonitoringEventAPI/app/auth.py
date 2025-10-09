import time
from jose import JWTError, jwt, ExpiredSignatureError
from OpenSSL import crypto
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.logger import get_app_logger
from app.config import get_settings

logger = get_app_logger()
settings = get_settings()

def _get_public_key(filepath: str) -> bytes:
    with open(filepath, "rb") as cert_file:
        cert = cert_file.read()

    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    pub_key_obj = certificate.get_pubkey()
    return crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key_obj)

async def no_auth_dependency() -> None:
    """
    An asynchronous dependency function that performs no authentication.

    Returns:
        None: Indicates no authentication is performed.
    """
    return None

async def verify_token(public_key: bytes, alg: str, credentials: HTTPAuthorizationCredentials) -> None:
    """
    Verifies a JWT token using the provided public key and algorithm.

    Attempts to decode the token up to 3 times if the token is not yet valid (`nbf` claim).
    Logs the token and authorization status. Raises HTTPException with status 401 if the token
    is expired or invalid.

    Args:
        public_key (bytes): The public key used to verify the JWT signature.
        alg (str): The algorithm used for JWT decoding.
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the token.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    token = credentials.credentials
    logger.info("token is: %s", token)
    retries = 0
    while (retries < 3):
        try:
            jwt.decode(token, public_key, algorithms=[alg])
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

def get_authentication_dependency():
    """
    Returns an authentication dependency function for FastAPI routes.
    If authentication is disabled in the settings, returns a no-op dependency.
    Otherwise, returns an async dependency that verifies JWT tokens using the provided public key and algorithm.
    Returns:
        Callable: A dependency function for FastAPI route authentication.
    """
    if not settings.auth_enabled:
        return no_auth_dependency
    
    PUB_KEY_PATH :str = settings.pub_key_path
    ALGORITHM :str = settings.algorithm

    PUB_KEY = _get_public_key(PUB_KEY_PATH)

    async def _auth_dependency(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> None:
        await verify_token(PUB_KEY, ALGORITHM, credentials)

    return _auth_dependency
