from src.modules.curso.create_curso.app.create_curso_viewmodel import CreateCursoViewmodel
from src.shared.domain.entities.curso import Curso


class TestCreateCursoViewmodel:
    def test_to_dict_contains_expected_fields(self):
        curso = Curso(código='MAT', nome='Matemática')

        response = CreateCursoViewmodel(curso).to_dict()

        assert response['código'] == 'MAT'
        assert response['nome'] == 'Matemática'
