from src.shared.infra.external.dynamo.single_table_keys import (
    GLOBAL_OWNER,
    SK_ENTITY_RECORD,
    EntityKind,
    build_partition_key,
    normalize_owner_id,
    strip_dynamo_metadata,
)


def test_normalize_owner_id_none_vai_para_global():
    assert normalize_owner_id(None) == GLOBAL_OWNER
    assert normalize_owner_id("") == GLOBAL_OWNER
    assert normalize_owner_id("  ") == GLOBAL_OWNER


def test_normalize_owner_id_remove_hash():
    assert normalize_owner_id("a#b") == "a_b"


def test_build_partition_key():
    assert (
        build_partition_key(GLOBAL_OWNER, EntityKind.CURSO, "ECM")
        == "GLOBAL#CURSO#ECM"
    )
    assert (
        build_partition_key("u1", EntityKind.DISCIPLINA, "P1")
        == "u1#DISCIPLINA#P1"
    )


def test_sk_fixa_metadata():
    assert SK_ENTITY_RECORD == "METADATA"


def test_strip_dynamo_metadata():
    assert strip_dynamo_metadata(
        {"pk": "x", "sk": "y", "entity_type": "CURSO", "nome": "N"}
    ) == {"nome": "N"}
