import pytest

from src.modules.grade_optimizer.app.grade_optmizer_viewmodel import GradeOptmizerViewmodel
from src.shared.domain.entities.nota import Nota


class TestGradeOptimizerViewmodel:

    def test_grade_optmizer_viewmodel(self):
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
                            'message':'o algoritmo retornou uma combinação válida de notas'
                            }
        
    def test_grade_optmizer_viewmodel_grades_not_found(self):
        notas = [
        ]
        
        viewmodel = GradeOptmizerViewmodel(notas).to_dict()
        
        assert viewmodel == {
                            'notas':[
                            ],
                            'message':'o algoritmo não encontrou uma combinação possível de notas'
                            }