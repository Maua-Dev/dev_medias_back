import pytest
from pydantic import ValidationError

from src.shared.domain.entities.curso import Curso


def _assert_single_error(errors, *, type_, loc, input_):
    assert len(errors) == 1
    err = errors[0]
    assert err["type"] == type_
    assert err["loc"] == loc
    assert err["input"] == input_


class TestCurso:
    def test_curso_creation(self):
        curso = Curso(código="ECM", nome="Engenharia de Computação")
        assert curso.código == "ECM"
        assert curso.nome == "Engenharia de Computação"

    def test_curso_código_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Curso(código=["não é str"], nome="Engenharia de Computação")
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("código",),
            input_=["não é str"],
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()

    def test_curso_nome_invalido(self):
        with pytest.raises(ValidationError) as exc_info:
            Curso(código="ECM", nome={"invalid": True})
        _assert_single_error(
            exc_info.value.errors(),
            type_="string_type",
            loc=("nome",),
            input_={"invalid": True},
        )
        assert "string" in exc_info.value.errors()[0]["msg"].lower()
