import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.modules.grade_optimizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.Nota import Nota
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.functions.utils import Utils
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.solucionador import Solucionador


class TestGradeOptimizerUsecase:

    def test_possible_grade(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        notas_resp = usecase(notas_que_tenho=[P1, T1, T2], notas_que_quero=[P2, P3, T3, P4, T4], media_desejada=media_desejada)

        assert abs(Utils.media(notas_resp + [P1, T1, T2]) - media_desejada) <= Solucionador.ERR_MAX

    # def test_get_user_not_found(self):
    #     repo = UserRepositoryMock()
    #     usecase = GetUserUsecase(repo)
    #
    #     with pytest.raises(NoItemsFound):
    #         user = usecase(user_id=999)
    #
    # def test_get_user_invalid_id(self):
    #     repo = UserRepositoryMock()
    #     usecase = GetUserUsecase(repo)
    #
    #     with pytest.raises(EntityError):
    #         user = usecase(user_id="invalid")
