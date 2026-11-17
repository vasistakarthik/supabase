
import time
import logging
import inspect
from functools import wraps

logger = logging.getLogger(__name__)


def measure_execution_time(func):

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):

            start_time = time.perf_counter()

            try:
                return await func(*args, **kwargs)

            finally:
                end_time = time.perf_counter()

                execution_time = end_time - start_time

                logger.info(
                    "[PERFORMANCE] %s executed in %.4f seconds",
                    func.__name__,
                    execution_time
                )

        return async_wrapper

    @wraps(func)
    def sync_wrapper(*args, **kwargs):

        start_time = time.perf_counter()

        try:
            return func(*args, **kwargs)

        finally:
            end_time = time.perf_counter()

            execution_time = end_time - start_time

            logger.info(
                "[PERFORMANCE] %s executed in %.4f seconds",
                func.__name__,
                execution_time
            )

    return sync_wrapper
