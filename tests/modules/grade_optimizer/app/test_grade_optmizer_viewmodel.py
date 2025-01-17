import pytest

from src.modules.grade_optmizer.app.grade_optmizer_viewmodel import GradeOptmizerViewmodel
from src.shared.domain.entities.boletim import Boletim
from src.shared.domain.entities.nota import Nota


class TestGradeOptimizerViewmodel:

    def test_grade_optmizer_viewmodel(self):
        P1 = Nota(peso=0.4, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.6, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.4, valor=None)
        T2 = Nota(peso=0.6, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        peso_prova = P1.peso + P2.peso
        peso_trabalho = T1.peso + T2.peso

        boletim = Boletim(peso_prova=peso_prova, peso_trabalho=peso_trabalho, provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        
        viewmodel = GradeOptmizerViewmodel(boletim).to_dict()
        
        assert viewmodel == {
            "notas":{
                "provas":[
                    {
                        "valor":7.5,
                        "peso":0.6
                    }
                ],
                "trabalhos":[
                    {
                        "valor":7.5,
                        "peso":0.4
                    },
                    {
                        "valor":8,
                        "peso":0.6
                    }
                ]
            },
            "message":"O algoritmo retornou uma combinação válida de notas"
        }
        
    def test_grade_optmizer_viewmodel_grades_somente_provas(self):
        P1 = Nota(peso=0.2, valor=1.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.2, valor=None)
        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = []
        
        peso_prova = P1.peso + P2.peso + P3.peso + P4.peso
        peso_trabalho = 1.0

        boletim = Boletim(peso_prova=peso_prova, peso_trabalho=peso_trabalho, provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        
        viewmodel = GradeOptmizerViewmodel(boletim).to_dict()
        
        assert viewmodel == {
            "notas":{
                "provas":[
                    {
                        "valor":7.5,
                        "peso":0.2
                    },
                    {
                        "valor":7.5,
                        "peso":0.3
                    },
                    {
                        "valor":8,
                        "peso":0.3
                    }
                ],
                "trabalhos":[
                    
                ]
            },
            "message":"O algoritmo retornou uma combinação válida de notas"
        }
        
    def test_grade_optmizer_viewmodel_grades_somente_trabalhos(self):
        T1 = Nota(peso=0.2, valor=1.0)
        provas_que_tenho = []
        trabalhos_que_tenho = [T1]
        
        
        T2 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.3, valor=None)
        T4 = Nota(peso=0.3, valor=None)
        provas_que_quero = []
        trabalhos_que_quero = [T2, T3, T4]
        
        peso_prova = 1.0
        peso_trabalho = T1.peso + T2.peso + T3.peso + T4.peso

        boletim = Boletim(peso_prova=peso_prova, peso_trabalho=peso_trabalho, provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        
        viewmodel = GradeOptmizerViewmodel(boletim).to_dict()
        
        assert viewmodel == {
            "notas":{
                "provas":[
                ],
                "trabalhos":[
                    {
                        "valor":7.5,
                        "peso":0.2
                    },
                    {
                        "valor":7.5,
                        "peso":0.3
                    },
                    {
                        "valor":8,
                        "peso":0.3
                    }
                ]
            },
            "message":"O algoritmo retornou uma combinação válida de notas"
        }
        
    def test_grade_optmizer_viewmodel_grades_not_found(self):
        T1 = Nota(peso=0.2, valor=1.0)
        provas_que_tenho = []
        trabalhos_que_tenho = [T1]
        
        
        T2 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.3, valor=None)
        T4 = Nota(peso=0.3, valor=None)
        provas_que_quero = []
        trabalhos_que_quero = [T2, T3, T4]
        
        peso_prova = 1.0
        peso_trabalho = T1.peso + T2.peso + T3.peso + T4.peso

        boletim = Boletim(peso_prova=peso_prova, peso_trabalho=peso_trabalho, provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        
        viewmodel = GradeOptmizerViewmodel(boletim).to_dict()
        
        assert viewmodel == {
                'notas': {
                    'provas': [],
                    'trabalhos': [],
                },
                'message': "O algoritmo não encontrou uma combinação possível de notas"
            }