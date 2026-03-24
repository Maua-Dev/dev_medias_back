import pytest
from unittest.mock import MagicMock
from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.modules.genetic_algorithm.app.genetic_algorithm_viewmodel import GeneticAlgorithmViewmodel


def make_boletim(provas=None, trabalhos=None, message="Combinação válida"):
    boletim = MagicMock(spec=Boletim_GA)
    boletim.provas = provas if provas is not None else [{"valor": 8.0, "peso": 0.5}, {"valor": 7.0, "peso": 0.5}]
    boletim.trabalhos = trabalhos if trabalhos is not None else [{"valor": 9.0, "peso": 1.0}]
    boletim.message = message
    return boletim


class TestGeneticAlgorithmViewmodel:

    def test_to_dict_structure(self):
        boletim = make_boletim()
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert "notas" in result
        assert "provas" in result["notas"]
        assert "trabalhos" in result["notas"]
        assert "message" in result

    def test_provas_correct(self):
        provas = [{"valor": 8.0, "peso": 0.5}]
        boletim = make_boletim(provas=provas)
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["notas"]["provas"] == provas

    def test_trabalhos_correct(self):
        trabalhos = [{"valor": 9.0, "peso": 1.0}]
        boletim = make_boletim(trabalhos=trabalhos)
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["notas"]["trabalhos"] == trabalhos

    def test_provas_and_trabalhos_are_different(self):
        boletim = make_boletim()
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["notas"]["provas"] != result["notas"]["trabalhos"]

    def test_message_correct(self):
        boletim = make_boletim(message="O algoritmo retornou uma combinação válida de notas")
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["message"] == "O algoritmo retornou uma combinação válida de notas"

    def test_empty_provas(self):
        boletim = make_boletim(provas=[])
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["notas"]["provas"] == []

    def test_empty_trabalhos(self):
        boletim = make_boletim(trabalhos=[])
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert result["notas"]["trabalhos"] == []

    def test_multiple_provas(self):
        provas = [{"valor": round(i * 1.5, 2), "peso": 0.25} for i in range(4)]
        boletim = make_boletim(provas=provas)
        result = GeneticAlgorithmViewmodel(boletim).to_dict()

        assert len(result["notas"]["provas"]) == 4
        assert result["notas"]["provas"] == provas