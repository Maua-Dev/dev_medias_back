"""
Nome físico da tabela single-table do catálogo acadêmico.

Deve bater com `iac/components/dynamo_construct.py` (CDK). Se mudar o prefixo, atualize os dois.
"""

ACADEMIC_CATALOG_TABLE_PREFIX = "DevMediasAcademicCatalogTable"


def physical_table_name(stage: str) -> str:
    """
    Mesmo padrão do CDK: ``{PREFIX}-{stage.lower()}`` (ex.: DevMediasAcademicCatalogTable-dev).
    """
    s = (stage or "test").strip().lower()
    return f"{ACADEMIC_CATALOG_TABLE_PREFIX}-{s}"
