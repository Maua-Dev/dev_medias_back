import pytest

from src.modules.plans_extractor.app.helper.criterion_structure import (
    apply_criterion_structure,
    determinar_estrutura_provas_trabalhos,
    extract_criterion_code,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Critério de aprovação: C4/2015\nQuantidade de Trabalhos: 2", "C4"),
        ("Critério de aprovação: A2/2007\nPeso de MT(kt):1", "A2"),
        ("Critério de aprovação: B1/2010", "B1"),
        ("sem codigo aqui", None),
    ],
)
def test_extract_criterion_code(text, expected):
    assert extract_criterion_code(text) == expected


@pytest.mark.parametrize(
    ("criterio", "num_provas", "tem_trabalhos"),
    [
        ("A1", 0, True),
        ("A4", 0, True),
        ("B1", 2, False),
        ("B2", 4, False),
        ("B3", 1, False),
        ("B9", 2, False),
        ("C1", 2, True),
        ("C2", 4, True),
        ("C3", 1, True),
        ("C4", 2, True),
        ("C8", 2, True),
    ],
)
def test_determinar_estrutura_provas_trabalhos(criterio, num_provas, tem_trabalhos):
    assert determinar_estrutura_provas_trabalhos(criterio, "A") == (num_provas, tem_trabalhos)


def test_determinar_estrutura_e_familia_raises():
    with pytest.raises(ValueError, match="specific handling"):
        determinar_estrutura_provas_trabalhos("E1", "A")


def test_apply_criterion_c4_forces_two_exams_and_keeps_assignments():
    payload = {
        "period": "A",
        "examWeight": 0.7,
        "assignmentWeight": 0.3,
        "exams": [
            {"name": "P1", "weight": 0.25},
            {"name": "P2", "weight": 0.25},
            {"name": "P3", "weight": 0.25},
            {"name": "P4", "weight": 0.25},
        ],
        "assignments": [{"name": "K1", "weight": 1.0}],
    }
    result = apply_criterion_structure(payload, "Critério de aprovação: C4/2015")

    assert len(result["exams"]) == 2
    assert result["assignments"] == [{"name": "K1", "weight": 1.0}]
    assert result["examWeight"] == 0.7
    assert result["assignmentWeight"] == 0.3


def test_apply_criterion_a_star_forces_zero_exams_with_assignments():
    payload = {
        "period": "A",
        "examWeight": 0.5,
        "assignmentWeight": 0.5,
        "exams": [{"name": "P1", "weight": 1.0}],
        "assignments": [{"name": "K1", "weight": 1.0}],
    }
    result = apply_criterion_structure(payload, "Critério de aprovação: A2/2007")

    assert result["exams"] == []
    assert result["examWeight"] == 0
    assert result["exam_weight"] == 0
    assert result["assignments"] == [{"name": "K1", "weight": 1.0}]


def test_apply_criterion_b1_forces_two_exams_without_assignments():
    payload = {
        "period": "S",
        "examWeight": 0.8,
        "assignmentWeight": 0.2,
        "exams": [{"name": "P1", "weight": 1.0}],
        "assignments": [{"name": "T1", "weight": 1.0}],
    }
    result = apply_criterion_structure(payload, "Critério de aprovação: B1/2010")

    assert [exam["name"] for exam in result["exams"]] == ["P1", "P2"]
    assert result["assignments"] == []
    assert result["assignmentWeight"] == 0
    assert result["assignment_weight"] == 0


def test_apply_criterion_ignores_conflicting_free_text_counts():
    criteria = (
        "Critério de aprovação: C3/2015\n"
        "O aluno fará quatro provas bimestrais e nenhum trabalho."
    )
    payload = {
        "period": "A",
        "examWeight": 0.6,
        "assignmentWeight": 0.4,
        "exams": [
            {"name": "P1", "weight": 0.25},
            {"name": "P2", "weight": 0.25},
            {"name": "P3", "weight": 0.25},
            {"name": "P4", "weight": 0.25},
        ],
        "assignments": [],
    }
    result = apply_criterion_structure(payload, criteria)

    assert len(result["exams"]) == 1
    assert result["exams"][0]["name"] == "P1"
