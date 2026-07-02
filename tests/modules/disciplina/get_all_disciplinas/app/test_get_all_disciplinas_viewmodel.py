from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_viewmodel import GetAllDisciplinasViewmodel
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


class TestGetAllDisciplinasViewmodel:
    def test_to_dict_returns_list(self):
        disciplinas = DisciplinaRepositoryMock().get_all_disciplinas()

        response = GetAllDisciplinasViewmodel(disciplinas).to_dict()

        assert isinstance(response, list)
        assert len(response) == 4

    def test_to_dict_contains_expected_fields(self):
        disciplinas = DisciplinaRepositoryMock().get_all_disciplinas()

        response = GetAllDisciplinasViewmodel(disciplinas).to_dict()

        assert response[0]["code"] == "ECM101"
        assert response[0]["name"] == "Engenharia de Computação"
        assert "exam_weight" in response[0]
        assert "assignment_weight" in response[0]
