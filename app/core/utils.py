from datetime import timedelta
from typing import Set, Callable
from redis import Redis
from redis.exceptions import LockError
from fastapi import FastAPI
from fastapi.openapi.utils import generate_operation_id
from fastapi.routing import APIRoute
from app.core.exception import TooManyRequests


def rate_limiter(func: Callable, redis: Redis, key: str, limit: int, period: timedelta):
    """
    Return the result of the function if the request limit is not exceeded else raise TooManyRequests exception

        Parameters:
            func (Callable): Function

            redis (Redis): Redis connection

            key (str): Redis key

            limit (int): count request in period

            period (timedelta): time to reset limit

        Returns: func(*args, **kwargs) or TooManyRequests exception
    """
    def request_is_limited(r: Redis, key: str, limit: int, period: timedelta) -> bool:
        """
        Using Generic cell rate algorithm

        Return True if the request limit is exceeded else False
            Parameters:
                r (Redis): Redis connection

                key (str): Redis key

                limit (int): count request in period

                period (timedelta): time to reset limit

            Return: Bool

        """
        period_in_seconds = int(period.total_seconds())
        t = r.time()[0]
        separation = round(period_in_seconds / limit)
        r.setnx(key, 0)
        try:
            with r.lock('lock:' + key, blocking_timeout=separation) as lock:
                tat = max(int(r.get(key)), t)
                if tat - t <= period_in_seconds - separation:
                    new_tat = max(tat, t) + separation
                    r.set(key, new_tat)
                    return False
                return True
        except LockError:
            return True

    def wrapper(*args, **kwargs):
        """
        Return the result of the function if the request limit is not exceeded else raise TooManyRequests
        """
        if request_is_limited(redis, key, limit, period):
            raise TooManyRequests()
        return func(*args, **kwargs)

    return wrapper


def request_is_limited(r: Redis, key: str, limit: int, period: timedelta) -> bool:
    """
        Using Generic cell rate algorithm

        Return True if the request limit is exceeded else False
            Parameters:
                r (Redis): Redis connection,
                key (str): Redis key,
                limit (int): count request in period,
                period (timedelta): time to reset limit

            Return: Bool
    """
    period_in_seconds = int(period.total_seconds())
    t = r.time()[0]
    separation = round(period_in_seconds / limit)
    r.setnx(key, 0)
    try:
        with r.lock('lock:' + key, blocking_timeout=separation) as lock:
            tat = max(int(r.get(key)), t)
            if tat - t <= period_in_seconds - separation:
                new_tat = max(tat, t) + separation
                r.set(key, new_tat)
                return False
            return True
    except LockError:
        return True


def remove_422_from_app(app: FastAPI) -> None:
    """
    Remove response with 422 status code if route have attributes __remove_422__ from openapi
    """
    openapi_schema = app.openapi()
    # remove HTTPValidationError schema
    del app.openapi_schema["components"]["schemas"]["HTTPValidationError"]
    # remove HTTPValidationError ValidationError
    del app.openapi_schema["components"]["schemas"]["ValidationError"]

    operation_ids_to_update: Set[str] = set()
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        methods = route.methods or ["GET"]
        if getattr(route.endpoint, "__remove_422__", None):
            for method in methods:
                operation_ids_to_update.add(generate_operation_id(route=route, method=method))
    paths = openapi_schema["paths"]
    for path, operations in paths.items():
        for method, metadata in operations.items():
            operation_id = metadata.get("operationId")
            if operation_id in operation_ids_to_update:
                metadata["responses"].pop("422", None)


def remove_422(func: Callable) -> Callable:
    """
    Decorator for remove response with 422 status code for route

    Example:
        @router.get('/')

        @remove_422

        def get_data():
            pass
    """
    func.__remove_422__ = True
    return func
