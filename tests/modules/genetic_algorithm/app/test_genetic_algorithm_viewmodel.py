
import pytest
from src.modules.genetic_algorithm.app.genetic_algorithm_viewmodel import GeneticAlgorithmViewmodel
from src.shared.domain.entities.boletim_ga import Boletim_GA


class TestGeneticAlgorithmViewmodel:

    def test_genetic_algorithm_viewmodel_basic(self):
        """Teste básico com provas e trabalhos"""
        boletim = Boletim_GA(
            current_tests=[6.0, 8.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.5, 8.0]
        boletim.calculated_assignments = [7.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel is not None
        assert "notas" in viewmodel
        assert "provas" in viewmodel["notas"]
        assert "trabalhos" in viewmodel["notas"]
        assert "peso provas" in viewmodel["notas"]
        assert "peso trabalhos" in viewmodel["notas"]
        assert "message" in viewmodel
        assert len(viewmodel["notas"]["provas"]) == 4
        assert len(viewmodel["notas"]["trabalhos"]) == 2

    def test_genetic_algorithm_viewmodel_only_tests(self):
        """Teste apenas com provas"""
        boletim = Boletim_GA(
            current_tests=[5.0],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.0, 7.5, 8.0]
        boletim.calculated_assignments = []
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["peso provas"] == 1.0
        assert viewmodel["notas"]["peso trabalhos"] == 0.0
        assert len(viewmodel["notas"]["provas"]) == 4
        assert len(viewmodel["notas"]["trabalhos"]) == 0

    def test_genetic_algorithm_viewmodel_only_assignments(self):
        """Teste apenas com trabalhos"""
        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[8.0, 9.0],
            num_remaining_tests=0,
            num_remaining_assignments=2,
            test_weight=0.0,
            assignment_weight=1.0,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = []
        boletim.calculated_assignments = [6.0, 5.0]
        boletim.target_avg = 6.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["peso provas"] == 0.0
        assert viewmodel["notas"]["peso trabalhos"] == 1.0
        assert len(viewmodel["notas"]["provas"]) == 0
        assert len(viewmodel["notas"]["trabalhos"]) == 4

    def test_genetic_algorithm_viewmodel_with_specific_weights(self):
        """Teste com pesos específicos"""
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=2,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=[0.2, 0.4, 0.4],
            spec_assignment_weight=[0.3, 0.3, 0.4]
        )
        
        boletim.calculated_tests = [7.5, 8.0]
        boletim.calculated_assignments = [7.5, 8.0]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["provas"][0]["peso"] == 0.2
        assert viewmodel["notas"]["provas"][1]["peso"] == 0.4
        assert viewmodel["notas"]["provas"][2]["peso"] == 0.4
        assert viewmodel["notas"]["trabalhos"][0]["peso"] == 0.3
        assert viewmodel["notas"]["trabalhos"][1]["peso"] == 0.3
        assert viewmodel["notas"]["trabalhos"][2]["peso"] == 0.4

    def test_genetic_algorithm_viewmodel_without_specific_weights(self):
        """Teste sem pesos específicos"""
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.5, 8.0]
        boletim.calculated_assignments = [7.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["provas"][0]["peso"] is None
        assert viewmodel["notas"]["provas"][1]["peso"] is None
        assert viewmodel["notas"]["trabalhos"][0]["peso"] is None

    def test_genetic_algorithm_viewmodel_message_valid_combination(self):
        """Teste mensagem de combinação válida (diferença <= 0.05)"""
        boletim = Boletim_GA(
            current_tests=[7.0],
            current_assignments=[7.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.5,
            assignment_weight=0.5,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.0]
        boletim.calculated_assignments = [7.0]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["message"] == "O algoritmo retornou uma combinação válida de notas"

    def test_genetic_algorithm_viewmodel_message_close_solution(self):
        """Teste mensagem de solução próxima (0.05 < diferença <= 0.2)"""
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[6.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.5,
            assignment_weight=0.5,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [6.5]
        boletim.calculated_assignments = [6.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert "solução próxima" in viewmodel["message"]
        assert "diferença" in viewmodel["message"]

    def test_genetic_algorithm_viewmodel_message_no_close_solution(self):
        """Teste mensagem de solução não encontrada (diferença > 0.2)"""
        boletim = Boletim_GA(
            current_tests=[3.0],
            current_assignments=[3.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.5,
            assignment_weight=0.5,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [4.0]
        boletim.calculated_assignments = [4.0]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert "não conseguiu encontrar" in viewmodel["message"]
        assert "diferença" in viewmodel["message"]

    def test_genetic_algorithm_viewmodel_rounded_values(self):
        """Teste se valores são arredondados para 2 casas decimais"""
        boletim = Boletim_GA(
            current_tests=[6.567],
            current_assignments=[7.893],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=[0.333, 0.667],
            spec_assignment_weight=[0.456, 0.544]
        )
        
        boletim.calculated_tests = [7.123]
        boletim.calculated_assignments = [8.456]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["provas"][0]["nota"] == 6.57
        assert viewmodel["notas"]["provas"][1]["nota"] == 7.12
        assert viewmodel["notas"]["trabalhos"][0]["nota"] == 7.89
        assert viewmodel["notas"]["trabalhos"][1]["nota"] == 8.46
        assert viewmodel["notas"]["provas"][0]["peso"] == 0.33
        assert viewmodel["notas"]["trabalhos"][0]["peso"] == 0.46

    def test_genetic_algorithm_viewmodel_high_target_average(self):
        """Teste com média desejada alta"""
        boletim = Boletim_GA(
            current_tests=[10.0, 10.0],
            current_assignments=[10.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [10.0, 10.0]
        boletim.calculated_assignments = [10.0]
        boletim.target_avg = 10.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["message"] == "O algoritmo retornou uma combinação válida de notas"
        assert all(p["nota"] == 10.0 for p in viewmodel["notas"]["provas"])
        assert all(t["nota"] == 10.0 for t in viewmodel["notas"]["trabalhos"])

    def test_genetic_algorithm_viewmodel_low_target_average(self):
        """Teste com média desejada baixa"""
        boletim = Boletim_GA(
            current_tests=[3.0],
            current_assignments=[4.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.5,
            assignment_weight=0.5,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [5.0]
        boletim.calculated_assignments = [5.5]
        boletim.target_avg = 5.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert "notas" in viewmodel
        assert "message" in viewmodel

    def test_genetic_algorithm_viewmodel_all_remaining(self):
        """Teste sem nenhuma nota atual"""
        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=2,
            test_weight=0.5,
            assignment_weight=0.5,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.0, 7.5, 8.0]
        boletim.calculated_assignments = [7.0, 7.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert len(viewmodel["notas"]["provas"]) == 3
        assert len(viewmodel["notas"]["trabalhos"]) == 2

    def test_genetic_algorithm_viewmodel_weights_sum(self):
        """Teste se os pesos de provas e trabalhos somam corretamente"""
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.5, 8.0]
        boletim.calculated_assignments = [7.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert viewmodel["notas"]["peso provas"] + viewmodel["notas"]["peso trabalhos"] == 1.0

    def test_genetic_algorithm_viewmodel_structure(self):
        """Teste estrutura completa do dicionário retornado"""
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=None,
            spec_assignment_weight=None
        )
        
        boletim.calculated_tests = [7.5]
        boletim.calculated_assignments = [7.5]
        boletim.target_avg = 7.0
        
        viewmodel = GeneticAlgorithmViewmodel(boletim).to_dict()
        
        assert isinstance(viewmodel, dict)
        assert isinstance(viewmodel["notas"], dict)
        assert isinstance(viewmodel["notas"]["provas"], list)
        assert isinstance(viewmodel["notas"]["trabalhos"], list)
        assert isinstance(viewmodel["notas"]["peso provas"], float)
        assert isinstance(viewmodel["notas"]["peso trabalhos"], float)
        assert isinstance(viewmodel["message"], str)
        
        for prova in viewmodel["notas"]["provas"]:
            assert "nota" in prova
            assert "peso" in prova
            
        for trabalho in viewmodel["notas"]["trabalhos"]:
            assert "nota" in trabalho
            assert "peso" in trabalho
