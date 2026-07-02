import pytest
from pydantic import ValidationError

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao


def _assert_single_error(errors, *, type_, loc, input_):
    assert len(errors) == 1
    err = errors[0]
    assert err["type"] == type_
    assert err["loc"] == loc
    assert err["input"] == input_


class TestDisciplina:
    def test_disciplina_creation(self):
        disciplina = Disciplina(
            course="ECM",
            name="Engenharia de Computação",
            code="ECM101",
            period="2024.1",
            exam_weight=0.6,
            assignment_weight=0.4,
            exams=[ItemAvaliacao(name="P1", weight=0.6)],
            assignments=[ItemAvaliacao(name="T1", weight=0.4)],
            courses={"ECM": 2024},
        )
        assert disciplina.course == "ECM"
        assert disciplina.name == "Engenharia de Computação"
        assert disciplina.code == "ECM101"
        assert disciplina.period == "2024.1"
        assert disciplina.exam_weight == 0.6
        assert disciplina.assignment_weight == 0.4
        assert disciplina.exams == [ItemAvaliacao(name="P1", weight=0.6)]
        assert disciplina.assignments == [ItemAvaliacao(name="T1", weight=0.4)]
        assert disciplina.courses == {"ECM": 2024}

    def test_disciplina_course_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course=["não é str"],
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("course",),
            input_=["não é str"],
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_name_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name=["não é str"],
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("name",),
            input_=["não é str"],
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_code_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code=["não é str"],
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("code",),
            input_=["não é str"],
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_period_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period=["não é str"],
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("period",),
            input_=["não é str"],
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_exam_weight_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=["não é float"],
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="float_type",
            loc=("exam_weight",),
            input_=["não é float"],
        )
        # Pydantic v2 costuma dizer "valid number", não necessariamente "float"
        assert "number" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_assignment_weight_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=["não é float"],
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="float_type",
            loc=("assignment_weight",),
            input_=["não é float"],
        )
        assert "number" in exc_info.value.errors()[0]["msg"].lower()

    def test_disciplina_exams_invalido(self):
        invalid_item = ["não é ItemAvaliacao"]
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[invalid_item],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="model_type",
            loc=("exams", 0),
            input_=invalid_item,
        )

    def test_disciplina_assignments_invalido(self):
        invalid_item = ["não é ItemAvaliacao"]
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[invalid_item],
                courses={"ECM": 2024},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="model_type",
            loc=("assignments", 0),
            input_=invalid_item,
        )

    def test_disciplina_courses_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Disciplina(
                course="ECM",
                name="Engenharia de Computação",
                code="ECM101",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": ["não é int"]},
            )
        _assert_single_error(
            exc_info.value.errors(),
            type_="int_type",
            loc=("courses", "ECM"),
            input_=["não é int"],
        )
        assert "integer" in exc_info.value.errors()[0]["msg"].lower()
