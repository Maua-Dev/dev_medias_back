import pytest

from src.modules.grade_optimizer.app.grade_optmizer_viewmodel import GradeOptmizerViewmodel
from src.shared.domain.entities.nota import Nota


class TestGradeOptimizerViewmodel:

    def test_possible_grade_viewmodel(self):
        notas = [
            Nota(peso=0.12, valor=6.0),
            Nota(peso=0.08, valor=6.0),
            Nota(peso=0.08, valor=6.0),
        ]
        
        viewmodel = GradeOptmizerViewmodel(notas).to_dict()
        
        assert viewmodel == {
                            'notas':[
                                {
                                    'valor':6.0,
                                    'peso':0.12
                                },
                                {
                                    'valor':6.0,
                                    'peso':0.08
                                },
                                {
                                    'valor':6.0,
                                    'peso':0.08
                                }
                            ],
                            'message':'the algorithm retrieved a possible combination of grades successfully'
                            }