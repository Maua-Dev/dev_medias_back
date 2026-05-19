"""Lambda entrypoint — delegates to course_extractor (handler name required by IaC)."""

from .course_extractor import lambda_handler

__all__ = ["lambda_handler"]
