"""Lambda entrypoint — Dynamo Academic Catalog → legacy allSubjects/courses JSON on S3."""

from .export_legacy_catalog_controller import ExportLegacyCatalogController
from .export_legacy_catalog_usecase import ExportLegacyCatalogUsecase

usecase = ExportLegacyCatalogUsecase()
controller = ExportLegacyCatalogController(usecase)


def lambda_handler(event, context):
    return controller(event, context)
