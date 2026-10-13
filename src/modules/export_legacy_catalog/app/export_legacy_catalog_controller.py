from .export_legacy_catalog_usecase import ExportLegacyCatalogUsecase


class ExportLegacyCatalogController:
    def __init__(self, usecase: ExportLegacyCatalogUsecase) -> None:
        self.usecase = usecase

    def __call__(self, event=None, context=None) -> dict:
        return self.usecase()
