from src.shared.helpers.legacy_catalog.convert_to_legacy_json import (
    build_legacy_catalog,
    convert_disciplina,
)


def test_convert_disciplina_short_codes_and_percent_weights():
    raw = {
        "code": "EFB2001",
        "name": "Cálculo Integral Aplicado",
        "course": "Engenharia de Produção",
        "period": "S",
        "exam_weight": 0.7,
        "assignment_weight": 0.3,
        "exams": [
            {"name": "Prova 1", "weight": 0.4},
            {"name": "Prova Substitutiva", "weight": 1.0},
            {"name": "P2", "weight": 0.6},
        ],
        "assignments": [
            {"name": "Trabalho 1", "weight": 0.5},
            {"name": "K2", "weight": 0.5},
        ],
        "courses": {"EPM": 1, "ECM": "1"},
    }

    subject, meta = convert_disciplina(raw)

    assert subject["examWeight"] == 70.0
    assert subject["assignmentWeight"] == 30.0
    assert [e["name"] for e in subject["exams"]] == ["P1", "P2"]
    assert [a["name"] for a in subject["assignments"]] == ["T1", "K2"]
    assert subject["courses"] == {"EPM": 1, "ECM": 1}
    assert "Prova Substitutiva" in meta["dropped_substitutive_exams"]


def test_build_legacy_catalog_skips_custom_and_non_global():
    items = [
        {
            "pk": "GLOBAL#DISCIPLINA#AAA001",
            "entity_type": "DISCIPLINA",
            "code": "AAA001",
            "name": "Alpha",
            "course": "Test",
            "period": "A",
            "exam_weight": 1,
            "assignment_weight": 0,
            "exams": [{"name": "P1", "weight": 1}],
            "assignments": [],
            "courses": {"CIC": 1},
            "is_custom": False,
        },
        {
            "pk": "user-1#DISCIPLINA#CUSTOM1",
            "entity_type": "DISCIPLINA",
            "code": "CUSTOM1",
            "name": "Custom",
            "is_custom": True,
            "exam_weight": 1,
            "assignment_weight": 0,
            "exams": [],
            "assignments": [],
            "courses": {},
        },
        {
            "pk": "GLOBAL#CURSO#CIC",
            "entity_type": "CURSO",
            "código": "CIC",
            "nome": "Ciência da Computação",
        },
    ]

    subjects, courses, meta = build_legacy_catalog(items)

    assert list(subjects) == ["AAA001"]
    assert courses == {"CIC": "Ciência da Computação"}
    assert meta["skipped_non_global_or_custom"] == 1
    assert meta["subjects_count"] == 1
    assert meta["courses_count"] == 1
