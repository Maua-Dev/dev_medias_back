import pytest

from src.modules.plans_extractor.app.parser import build_disciplina


def _payload(**overrides):
    base = {
        "course": "Análise e Desenvolvimento de Sistemas",
        "name": "Algoritmos",
        "code": "ADS1003",
        "period": "A",
        "examWeight": 50,
        "assignmentWeight": 50,
        "exams": [
            {"name": "P1", "weight": 0.5},
            {"name": "P2", "weight": 0.5},
        ],
        "assignments": [
            {"name": "T1", "weight": 0.5},
            {"name": "T2", "weight": 0.5},
        ],
    }
    base.update(overrides)
    return base


@pytest.mark.parametrize(
    ("exam_weight", "assignment_weight", "expected_exam", "expected_assignment"),
    [
        (50, 50, 0.5, 0.5),
        (60, 40, 0.6, 0.4),
        (70, 30, 0.7, 0.3),
    ],
)
def test_normaliza_pesos_globais_para_escala_0_a_1(
    exam_weight, assignment_weight, expected_exam, expected_assignment
):
    disciplina = build_disciplina(
        _payload(examWeight=exam_weight, assignmentWeight=assignment_weight),
        courses={"ADS": 1},
    )

    assert disciplina.exam_weight == pytest.approx(expected_exam)
    assert disciplina.assignment_weight == pytest.approx(expected_assignment)


def test_aplica_guard_rail_em_pesos_internos_de_exams_e_assignments():
    disciplina = build_disciplina(
        _payload(
            period="A",
            exams=[
                {"name": "P1", "weight": 0},
                {"name": "P2", "weight": 0},
            ],
            assignments=[
                {"name": "T1", "weight": 40},
                {"name": "T2", "weight": 60},
            ],
        ),
        courses={"ADS": 1},
    )

    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.4, 0.6])
    assert [assignment.weight for assignment in disciplina.assignments] == pytest.approx([0.4, 0.6])


def test_cenario_ads1003_periodo_a_com_duas_provas_iguais_aplica_correcao():
    disciplina = build_disciplina(
        _payload(
            period="A",
            exams=[
                {"name": "P1", "weight": 0.5},
                {"name": "P2", "weight": 0.5},
            ],
        ),
        courses={"ADS": 1},
    )

    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.4, 0.6])


def test_resposta_bedrock_incompleta_faz_fallback_para_zero():
    disciplina = build_disciplina(
        _payload(
            examWeight=None,
            assignmentWeight=None,
            exams=[{"name": "P1", "weight": 1}],
            assignments=[{"name": "T1", "weight": 1}],
        ),
        courses={"ADS": 1},
    )

    assert disciplina.exam_weight == 0
    assert disciplina.assignment_weight == 0
    assert disciplina.exams == []
    assert disciplina.assignments == []


def test_remove_provas_e_trabalhos_substitutivos():
    disciplina = build_disciplina(
        _payload(
            exams=[
                {"name": "P1", "weight": 0.4},
                {"name": "Prova Substitutiva", "weight": 0.6},
            ],
            assignments=[
                {"name": "T1", "weight": 0.5},
                {"name": "Trabalho Substitutivo", "weight": 0.5},
            ],
        ),
        courses={"ADS": 1},
    )

    assert [exam.name for exam in disciplina.exams] == ["P1"]
    assert [exam.weight for exam in disciplina.exams] == pytest.approx([1.0])
    assert [assignment.name for assignment in disciplina.assignments] == ["T1"]
    assert [assignment.weight for assignment in disciplina.assignments] == pytest.approx([1.0])


def test_trunca_pesos_para_tres_casas_sem_arredondar_para_cima():
    disciplina = build_disciplina(
        _payload(
            exams=[
                {"name": "P1", "weight": 1},
                {"name": "P2", "weight": 1},
                {"name": "P3", "weight": 1},
            ],
            assignments=[
                {"name": "T1", "weight": 1},
                {"name": "T2", "weight": 1},
                {"name": "T3", "weight": 1},
            ],
            examWeight=33.34,
            assignmentWeight=66.66,
        ),
        courses={"ADS": 1},
    )

    assert disciplina.exam_weight == pytest.approx(0.333)
    assert disciplina.assignment_weight == pytest.approx(0.666)
    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.333, 0.333, 0.333])
    assert [assignment.weight for assignment in disciplina.assignments] == pytest.approx([0.333, 0.333, 0.333])
