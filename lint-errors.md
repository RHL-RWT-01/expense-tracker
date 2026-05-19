Rahul@Rahuls-PC MINGW64 ~/Desktop/python-practice (main)
$ black app
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\ftt\Desktop\python-practice\venv\Scripts\black.exe\__main__.py", line 2, in <module>
    from black import patched_main
  File "C:\Users\ftt\Desktop\python-practice\venv\Lib\site-packages\black\__init__.py", line 81, in <module>
    from black.ranges import (
    ...<4 lines>...
    )
  File "C:\Users\ftt\Desktop\python-practice\venv\Lib\site-packages\black\ranges.py", line 3, in <module>
    import difflib
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1022, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1155, in get_code
  File "<frozen importlib._bootstrap_external>", line 784, in _compile_bytecode
KeyboardInterrupt


(venv) 
Rahul@Rahuls-PC MINGW64 ~/Desktop/python-practice (main)
$ black app/
reformatted C:\Users\ftt\Desktop\python-practice\app\api\middleware\security.py
reformatted C:\Users\ftt\Desktop\python-practice\app\core\utils\helpers.py
reformatted C:\Users\ftt\Desktop\python-practice\app\core\database\mongodb.py
reformatted C:\Users\ftt\Desktop\python-practice\app\repositories\refresh_token.py
reformatted C:\Users\ftt\Desktop\python-practice\app\schemas\auth.py
reformatted C:\Users\ftt\Desktop\python-practice\app\services\category.py
reformatted C:\Users\ftt\Desktop\python-practice\app\services\analytics.py
reformatted C:\Users\ftt\Desktop\python-practice\app\repositories\category.py
reformatted C:\Users\ftt\Desktop\python-practice\app\repositories\transaction.py

All done! ✨ 🍰 ✨
9 files reformatted, 59 files left unchanged.
(venv) 
Rahul@Rahuls-PC MINGW64 ~/Desktop/python-practice (main)
$ ruff check app/
app\api\dependencies\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """API dependencies module."""
 2 |   
 3 | / from app.api.dependencies.auth import get_current_user, get_current_active_user
 4 | | from app.api.dependencies.services import (
 5 | |     get_auth_service,
 6 | |     get_user_service,
 7 | |     get_transaction_service,
 8 | |     get_category_service,
 9 | |     get_analytics_service,
10 | | )
11 | | 
12 | | __all__ = [
   | |_^ I001
13 |       "get_current_user",
14 |       "get_current_active_user",
   |
   = help: Organize imports

app\api\dependencies\auth.py:8:31: F401 [*] `app.core.database.get_database` imported but unused
   |
 6 | from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
 7 | 
 8 | from app.core.database import get_database
   |                               ^^^^^^^^^^^^ F401
 9 | from app.core.exceptions import AuthenticationException
10 | from app.core.security import JWTHandler
   |
   = help: Remove unused import: `app.core.database.get_database`

app\api\middleware\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Middleware module."""
 2 |   
 3 | / from app.api.middleware.logging import LoggingMiddleware
 4 | | from app.api.middleware.error_handler import ErrorHandlerMiddleware
 5 | | from app.api.middleware.request_id import RequestIDMiddleware
 6 | | from app.api.middleware.security import SecurityHeadersMiddleware
 7 | | 
 8 | | __all__ = [
   | |_^ I001
 9 |       "LoggingMiddleware",
10 |       "ErrorHandlerMiddleware",
   |
   = help: Organize imports

app\api\middleware\error_handler.py:3:1: UP035 [*] Import from `collections.abc` instead: `Callable`
  |
1 | """Centralized error handling middleware."""
2 | 
3 | from typing import Callable
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP035
4 | 
5 | from fastapi import Request
  |
  = help: Import from `collections.abc`

app\api\middleware\logging.py:4:1: UP035 [*] Import from `collections.abc` instead: `Callable`
  |
3 | import time
4 | from typing import Callable
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP035
5 | 
6 | from fastapi import Request, Response
  |
  = help: Import from `collections.abc`

app\api\middleware\request_id.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Request ID middleware for request tracing."""
 2 |   
 3 | / import uuid
 4 | | from typing import Callable
 5 | | 
 6 | | from fastapi import Request, Response
 7 | | from starlette.middleware.base import BaseHTTPMiddleware
 8 | | 
 9 | | import structlog
10 | | 
11 | | 
12 | | class RequestIDMiddleware(BaseHTTPMiddleware):
   | |_^ I001
13 |       """Middleware for adding unique request IDs."""
   |
   = help: Organize imports

app\api\middleware\request_id.py:4:1: UP035 [*] Import from `collections.abc` instead: `Callable`
  |
3 | import uuid
4 | from typing import Callable
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP035
5 | 
6 | from fastapi import Request, Response
  |
  = help: Import from `collections.abc`

app\api\middleware\security.py:3:1: UP035 [*] Import from `collections.abc` instead: `Callable`
  |
1 | """Security headers middleware."""
2 | 
3 | from typing import Callable
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP035
4 | 
5 | from fastapi import Request, Response
  |
  = help: Import from `collections.abc`

app\api\routes\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """API routes module."""
 2 |   
 3 | / from fastapi import APIRouter
 4 | | 
 5 | | from app.api.routes.auth import router as auth_router
 6 | | from app.api.routes.transactions import router as transactions_router
 7 | | from app.api.routes.categories import router as categories_router
 8 | | from app.api.routes.analytics import router as analytics_router
 9 | | from app.api.routes.health import router as health_router
10 | | 
11 | | # Create main API router
   | |_^ I001
12 |   api_router = APIRouter(prefix="/api/v1")
   |
   = help: Organize imports

app\api\routes\analytics.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Analytics routes."""
 2 |   
 3 | / from typing import Annotated
 4 | | 
 5 | | from fastapi import APIRouter, Depends, Query
 6 | | 
 7 | | from app.api.dependencies import get_current_active_user, get_analytics_service
 8 | | from app.schemas.analytics import (
 9 | |     AnalyticsParams,
10 | |     CategoryBreakdownResponse,
11 | |     MonthlyTrendsResponse,
12 | |     SummaryResponse,
13 | | )
14 | | from app.schemas.base import ResponseSchema
15 | | from app.services.analytics import AnalyticsService
16 | | 
17 | | router = APIRouter(prefix="/analytics", tags=["Analytics"])
   | |_^ I001
   |
   = help: Organize imports

app\api\routes\categories.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Category routes."""
 2 |   
 3 | / from typing import Annotated
 4 | | 
 5 | | from fastapi import APIRouter, Depends
 6 | | 
 7 | | from app.api.dependencies import get_current_active_user, get_category_service
 8 | | from app.schemas.base import ResponseSchema
 9 | | from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
10 | | from app.services.category import CategoryService
11 | | 
12 | | router = APIRouter(prefix="/categories", tags=["Categories"])
   | |_^ I001
   |
   = help: Organize imports

app\api\validators\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Request validators module."""
2 |   
3 | / from app.api.validators.common import validate_object_id, validate_date_range
4 | | 
5 | | __all__ = ["validate_object_id", "validate_date_range"]
  | |_^ I001
  |
  = help: Organize imports

app\core\constants\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Application constants."""
2 |   
3 | / from app.core.constants.enums import TransactionType
4 | | from app.core.constants.defaults import DEFAULT_CATEGORIES
5 | | 
6 | | __all__ = ["TransactionType", "DEFAULT_CATEGORIES"]
  | |_^ I001
  |
  = help: Organize imports

app\core\logging\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Logging configuration module."""
2 |   
3 | / from app.core.logging.config import setup_logging, get_logger
4 | | 
5 | | __all__ = ["setup_logging", "get_logger"]
  | |_^ I001
  |
  = help: Organize imports

app\core\security\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Security module."""
2 |   
3 | / from app.core.security.password import PasswordHandler
4 | | from app.core.security.jwt import JWTHandler, TokenPayload
5 | | 
6 | | __all__ = ["PasswordHandler", "JWTHandler", "TokenPayload"]
  | |_^ I001
  |
  = help: Organize imports

app\core\security\jwt.py:4:20: F401 [*] `typing.Any` imported but unused
  |
3 | from datetime import UTC, datetime, timedelta
4 | from typing import Any
  |                    ^^^ F401
5 | 
6 | from jose import JWTError, jwt
  |
  = help: Remove unused import: `typing.Any`

app\core\utils\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Utility functions module."""
2 |   
3 | / from app.core.utils.helpers import generate_uuid, to_objectid, from_objectid
4 | | 
5 | | __all__ = ["generate_uuid", "to_objectid", "from_objectid"]
  | |_^ I001
  |
  = help: Organize imports

app\lifespan.py:4:1: UP035 [*] Import from `collections.abc` instead: `AsyncGenerator`
  |
3 | from contextlib import asynccontextmanager
4 | from typing import AsyncGenerator
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP035
5 | 
6 | from fastapi import FastAPI
  |
  = help: Import from `collections.abc`

app\lifespan.py:16:20: ARG001 Unused function argument: `app`
   |
15 | @asynccontextmanager
16 | async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
   |                    ^^^ ARG001
17 |     """Manage application startup and shutdown."""
18 |     # Startup
   |

app\main.py:11:5: F401 [*] `app.api.middleware.ErrorHandlerMiddleware` imported but unused
   |
10 | from app.api.middleware import (
11 |     ErrorHandlerMiddleware,
   |     ^^^^^^^^^^^^^^^^^^^^^^ F401
12 |     LoggingMiddleware,
13 |     RequestIDMiddleware,
   |
   = help: Remove unused import: `app.api.middleware.ErrorHandlerMiddleware`

app\main.py:45:33: ARG001 Unused function argument: `request`
   |
44 | @app.exception_handler(AppException)
45 | async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
   |                                 ^^^^^^^ ARG001
46 |     """Handle application exceptions."""
47 |     return JSONResponse(
   |

app\models\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
  |
1 |   """Database models module."""
2 |   
3 | / from app.models.user import UserModel
4 | | from app.models.transaction import TransactionModel
5 | | from app.models.category import CategoryModel
6 | | from app.models.refresh_token import RefreshTokenModel
7 | | 
8 | | __all__ = ["UserModel", "TransactionModel", "CategoryModel", "RefreshTokenModel"]
  | |_^ I001
  |
  = help: Organize imports

app\repositories\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Repository layer module."""
 2 |   
 3 | / from app.repositories.base import BaseRepository
 4 | | from app.repositories.user import UserRepository
 5 | | from app.repositories.transaction import TransactionRepository
 6 | | from app.repositories.category import CategoryRepository
 7 | | from app.repositories.refresh_token import RefreshTokenRepository
 8 | | 
 9 | | __all__ = [
   | |_^ I001
10 |       "BaseRepository",
11 |       "UserRepository",
   |
   = help: Organize imports

app\repositories\base.py:6:18: F401 [*] `bson.ObjectId` imported but unused
  |
4 | from typing import Any, Generic, TypeVar
5 | 
6 | from bson import ObjectId
  |                  ^^^^^^^^ F401
7 | from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
  |
  = help: Remove unused import: `bson.ObjectId`

app\repositories\category.py:6:18: F401 [*] `bson.ObjectId` imported but unused
  |
4 | from typing import Any
5 | 
6 | from bson import ObjectId
  |                  ^^^^^^^^ F401
7 | from motor.motor_asyncio import AsyncIOMotorDatabase
  |
  = help: Remove unused import: `bson.ObjectId`

app\repositories\transaction.py:7:18: F401 [*] `bson.ObjectId` imported but unused
  |
5 | from typing import Any
6 | 
7 | from bson import ObjectId
  |                  ^^^^^^^^ F401
8 | from motor.motor_asyncio import AsyncIOMotorDatabase
  |
  = help: Remove unused import: `bson.ObjectId`

app\repositories\user.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """User repository for database operations."""
 2 |   
 3 | / from datetime import UTC, datetime
 4 | | from typing import Any
 5 | | 
 6 | | from bson import ObjectId
 7 | | from motor.motor_asyncio import AsyncIOMotorDatabase
 8 | | 
 9 | | from app.repositories.base import BaseRepository
10 | | from app.core.utils.helpers import serialize_doc
11 | | 
12 | | 
13 | | class UserRepository(BaseRepository):
   | |_^ I001
14 |       """Repository for user-related database operations."""
   |
   = help: Organize imports

app\repositories\user.py:6:18: F401 [*] `bson.ObjectId` imported but unused
  |
4 | from typing import Any
5 | 
6 | from bson import ObjectId
  |                  ^^^^^^^^ F401
7 | from motor.motor_asyncio import AsyncIOMotorDatabase
  |
  = help: Remove unused import: `bson.ObjectId`

app\schemas\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Pydantic schemas module."""
 2 |   
 3 | / from app.schemas.base import ResponseSchema, PaginatedResponse, PaginationMeta
 4 | | from app.schemas.auth import (
 5 | |     LoginRequest,
 6 | |     RegisterRequest,
 7 | |     TokenResponse,
 8 | |     RefreshTokenRequest,
 9 | |     ChangePasswordRequest,
10 | | )
11 | | from app.schemas.user import UserResponse, UserUpdate
12 | | from app.schemas.transaction import (
13 | |     TransactionCreate,
14 | |     TransactionUpdate,
15 | |     TransactionResponse,
16 | |     TransactionListParams,
17 | | )
18 | | from app.schemas.category import (
19 | |     CategoryCreate,
20 | |     CategoryUpdate,
21 | |     CategoryResponse,
22 | | )
23 | | from app.schemas.analytics import (
24 | |     SummaryResponse,
25 | |     CategoryBreakdown,
26 | |     CategoryBreakdownResponse,
27 | |     MonthlyTrend,
28 | |     MonthlyTrendsResponse,
29 | |     AnalyticsParams,
30 | | )
31 | | 
32 | | __all__ = [
   | |_^ I001
33 |       # Base
34 |       "ResponseSchema",
   |
   = help: Organize imports

app\schemas\auth.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Authentication schemas."""
 2 |   
 3 | / import re
 4 | | from typing import Annotated
 5 | | 
 6 | | from pydantic import BaseModel, EmailStr, Field, field_validator
 7 | | 
 8 | | from app.core.constants.defaults import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
 9 | | 
10 | | 
11 | | class RegisterRequest(BaseModel):
   | |_^ I001
12 |       """User registration request schema."""
   |
   = help: Organize imports

app\services\__init__.py:3:1: I001 [*] Import block is un-sorted or un-formatted
   |
 1 |   """Service layer module."""
 2 |   
 3 | / from app.services.auth import AuthService
 4 | | from app.services.user import UserService
 5 | | from app.services.transaction import TransactionService
 6 | | from app.services.category import CategoryService
 7 | | from app.services.analytics import AnalyticsService
 8 | | 
 9 | | __all__ = [
   | |_^ I001
10 |       "AuthService",
11 |       "UserService",
   |
   = help: Organize imports

app\services\analytics.py:6:20: F401 [*] `typing.Any` imported but unused
  |
4 | from datetime import datetime
5 | from decimal import Decimal
6 | from typing import Any
  |                    ^^^ F401
7 | 
8 | from app.core.logging import get_logger
  |
  = help: Remove unused import: `typing.Any`

app\services\auth.py:7:38: F401 [*] `app.core.constants.enums.TokenType` imported but unused
  |
6 | from app.core.config import get_settings
7 | from app.core.constants.enums import TokenType
  |                                      ^^^^^^^^^ F401
8 | from app.core.exceptions import AuthenticationException, ConflictException
9 | from app.core.logging import get_logger
  |
  = help: Remove unused import: `app.core.constants.enums.TokenType`

app\services\category.py:94:9: SIM102 Use a single `if` statement instead of nested `if` statements
    |
 93 |           # Check for name conflicts
 94 |           if "name" in update_data:
    |  _________^
 95 | |             if await self._category_repo.name_exists_for_user(
 96 | |                 update_data["name"],
 97 | |                 user_id,
 98 | |                 exclude_id=category_id,
 99 | |             ):
    | |______________^ SIM102
100 |                   raise ConflictException(f"Category '{update_data['name']}' already exists")
    |
    = help: Combine `if` statements using `and`

Found 34 errors.
[*] 31 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).