"""
Nome físico da tabela single-table do catálogo acadêmico.

Deve bater com `iac/components/dynamo_construct.py` (CDK). Se mudar o prefixo, atualize os dois.
"""

ACADEMIC_CATALOG_TABLE_PREFIX = "DevMediasAcademicCatalogTable"


def physical_table_name(stage: str, generation: str = "") -> str:
    """
    Mesmo padrão do CDK: ``{PREFIX}-{generation-}{stage.lower()}``
    (ex.: DevMediasAcademicCatalogTable-dev, DevMediasAcademicCatalogTable-v2-prod).
    Prefer ACADEMIC_CATALOG_TABLE_NAME from Lambda env when set by CDK.
    """
    s = (stage or "test").strip().lower()
    g = (generation or "").strip().lower()
    gen = f"{g}-" if g else ""
    return f"{ACADEMIC_CATALOG_TABLE_PREFIX}-{gen}{s}"
