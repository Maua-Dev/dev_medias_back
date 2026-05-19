"""Lambda entrypoint — delegates to course_extractor (handler name required by IaC)."""


def lambda_handler(event, context):
    from .course_extractor import lambda_handler as course_extractor_handler

    return course_extractor_handler(event, context)
