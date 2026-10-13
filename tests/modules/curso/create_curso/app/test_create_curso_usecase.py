import pytest

from src.modules.curso.create_curso.app.create_curso_usecase import CreateCursoUsecase
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


class TestCreateCursoUsecase:
    def test_create_curso_usecase_success(self):
        repository = CursoRepositoryMock()
        usecase = CreateCursoUsecase(repository)

        response = usecase(código='MAT', nome='Matemática')

        assert response.código == 'MAT'
        assert response.nome == 'Matemática'
        assert len(repository.cursos) == 4

    def test_create_curso_usecase_duplicated_item(self):
        repository = CursoRepositoryMock()
        usecase = CreateCursoUsecase(repository)

        with pytest.raises(DuplicatedItem):
            usecase(código='ECM', nome='Engenharia de Computação')
