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


def test_anual_quatro_provas_iguais_aplica_20_20_30_30():
    """EPM306-style: Bedrock invents 0.25×4; RN CEPE → 40/60 semestres."""
    disciplina = build_disciplina(
        _payload(
            period="A",
            examWeight=70,
            assignmentWeight=30,
            exams=[
                {"name": "P1", "weight": 0.25},
                {"name": "P2", "weight": 0.25},
                {"name": "P3", "weight": 0.25},
                {"name": "P4", "weight": 0.25},
            ],
            assignments=[
                {"name": "T1", "weight": 0.5},
                {"name": "T2", "weight": 0.5},
            ],
        ),
        courses={"EPM": 2},
    )

    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.2, 0.2, 0.3, 0.3])


def test_anual_com_pesos_explicitos_nao_uniformes_preserva():
    disciplina = build_disciplina(
        _payload(
            period="A",
            exams=[
                {"name": "P1", "weight": 0.1},
                {"name": "P2", "weight": 0.2},
                {"name": "P3", "weight": 0.3},
                {"name": "P4", "weight": 0.4},
            ],
        ),
        courses={"EPM": 2},
    )

    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.1, 0.2, 0.3, 0.4])


def test_semestral_quatro_provas_iguais_mantem_media_simples():
    disciplina = build_disciplina(
        _payload(
            period="S",
            exams=[
                {"name": "P1", "weight": 0.25},
                {"name": "P2", "weight": 0.25},
                {"name": "P3", "weight": 0.25},
                {"name": "P4", "weight": 0.25},
            ],
        ),
        courses={"ADS": 1},
    )

    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.25, 0.25, 0.25, 0.25])


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


def test_canonicaliza_nomes_descritivos_para_p_e_t():
    disciplina = build_disciplina(
        _payload(
            exams=[
                {"name": "Primeira Prova Bimestral", "weight": 0.4},
                {"name": "Segunda Avaliação", "weight": 0.6},
            ],
            assignments=[
                {"name": "Projeto do professor", "weight": 0.5},
                {"name": "Relatório final", "weight": 0.5},
            ],
            exams_code="C1/2007",
            study_plan_download_pdf_url="https://cdn.example/ADS/1/ADS1003.pdf",
        ),
        courses={"ADS": 1},
    )

    assert [exam.name for exam in disciplina.exams] == ["P1", "P2"]
    assert [assignment.name for assignment in disciplina.assignments] == ["T1", "T2"]
    assert disciplina.exams_code == "C1/2007"
    assert disciplina.study_plan_download_pdf_url == "https://cdn.example/ADS/1/ADS1003.pdf"


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
    # Annual + uniform exams → CEPE 40/60 groups (not Bedrock equal split).
    assert [exam.weight for exam in disciplina.exams] == pytest.approx([0.2, 0.2, 0.6])
    assert [assignment.weight for assignment in disciplina.assignments] == pytest.approx(
        [0.333, 0.333, 0.333]
    )
