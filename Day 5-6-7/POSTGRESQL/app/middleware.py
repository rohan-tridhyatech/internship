from __future__ import annotations

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Import the base class for middleware

# Custom Logging Middleware that logs request and response details


class LoggingMiddleware(BaseHTTPMiddleware):
    # Overriding the dispatch method to intercept and process requests and responses
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request details
        start_time = time.time()  # Record the time when the request is received
        # Log the HTTP method and URL
        print(f"Incoming request: {request.method} {request.url}")

        # Process the request and get the response
        response = await call_next(request)

        # Log the outgoing response details including the response status code and processing time
        # Calculate the time taken to process the request
        process_time = time.time() - start_time
        # Log the status code and process time
        print(f"Completed response: {response.status_code} in {process_time:.2f}s")

        # Return the response to the client
        return response
