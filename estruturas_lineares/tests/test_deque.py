import random
from collections import deque as deque_nativo

import pytest

from estruturas_lineares import EstruturaVaziaError
from estruturas_lineares.deque import CAPACIDADE_MINIMA, Deque, janela_deslizante_maximo


def test_deque_novo_esta_vazio() -> None:
    deque: Deque[int] = Deque()
    assert deque.vazio()
    assert len(deque) == 0
    assert not deque


def test_insercao_nas_duas_pontas() -> None:
    deque: Deque[int] = Deque()
    deque.adicionar_direita(2)
    deque.adicionar_esquerda(1)
    deque.adicionar_direita(3)
    deque.adicionar_esquerda(0)
    assert list(deque) == [0, 1, 2, 3]
    assert deque.primeiro() == 0
    assert deque.ultimo() == 3


def test_remocao_nas_duas_pontas() -> None:
    deque = Deque([1, 2, 3, 4])
    assert deque.remover_esquerda() == 1
    assert deque.remover_direita() == 4
    assert list(deque) == [2, 3]


@pytest.mark.parametrize("operacao", ["remover_esquerda", "remover_direita", "primeiro", "ultimo"])
def test_deque_vazio_levanta_erro(operacao: str) -> None:
    deque: Deque[int] = Deque()
    with pytest.raises(EstruturaVaziaError):
        getattr(deque, operacao)()


def test_indice_positivo_e_negativo() -> None:
    deque = Deque("abcde")
    assert deque[0] == "a"
    assert deque[4] == "e"
    assert deque[-1] == "e"
    assert deque[-5] == "a"


@pytest.mark.parametrize("indice", [5, -6, 100])
def test_indice_fora_do_deque(indice: int) -> None:
    with pytest.raises(IndexError):
        Deque("abcde")[indice]


def test_volta_no_buffer_circular() -> None:
    # Força o início a "dar a volta" no array sem redimensionar.
    deque: Deque[int] = Deque()
    for numero in range(CAPACIDADE_MINIMA):
        deque.adicionar_direita(numero)
    for _ in range(3):
        deque.remover_esquerda()
    for numero in range(3):
        deque.adicionar_direita(100 + numero)
    assert deque.capacidade == CAPACIDADE_MINIMA
    assert list(deque) == [3, 4, 5, 6, 7, 100, 101, 102]


def test_cresce_preservando_a_ordem_mesmo_com_volta() -> None:
    deque: Deque[int] = Deque()
    for numero in range(CAPACIDADE_MINIMA):
        deque.adicionar_esquerda(numero)
    deque.adicionar_esquerda(99)  # buffer cheio e "enrolado": precisa desenrolar ao copiar
    assert deque.capacidade == CAPACIDADE_MINIMA * 2
    assert list(deque) == [99, 7, 6, 5, 4, 3, 2, 1, 0]


def test_encolhe_depois_de_um_pico() -> None:
    deque = Deque(range(1_000))
    capacidade_no_pico = deque.capacidade
    while len(deque) > 2:
        deque.remover_direita()
    assert deque.capacidade < capacidade_no_pico
    assert deque.capacidade == CAPACIDADE_MINIMA
    assert list(deque) == [0, 1]


def test_comportamento_igual_ao_deque_nativo() -> None:
    # Teste de propriedade simples: sequência aleatória de operações
    # comparada com collections.deque, que serve de referência.
    gerador = random.Random(42)
    nosso: Deque[int] = Deque()
    referencia: deque_nativo[int] = deque_nativo()
    for passo in range(5_000):
        operacao = gerador.randrange(4)
        if operacao == 0:
            nosso.adicionar_direita(passo)
            referencia.append(passo)
        elif operacao == 1:
            nosso.adicionar_esquerda(passo)
            referencia.appendleft(passo)
        elif referencia and operacao == 2:
            assert nosso.remover_direita() == referencia.pop()
        elif referencia:
            assert nosso.remover_esquerda() == referencia.popleft()
        assert len(nosso) == len(referencia)
    assert list(nosso) == list(referencia)


@pytest.mark.parametrize(
    ("valores", "largura", "esperado"),
    [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([4, 2, 1], 1, [4, 2, 1]),
        ([4, 2, 1], 3, [4]),
        ([1, 2], 3, []),
        ([], 2, []),
        ([5, 5, 5], 2, [5, 5]),
    ],
)
def test_janela_deslizante_maximo(valores: list[int], largura: int, esperado: list[int]) -> None:
    assert janela_deslizante_maximo(valores, largura) == esperado


def test_janela_deslizante_confere_com_forca_bruta() -> None:
    gerador = random.Random(7)
    valores = [gerador.randint(-50, 50) for _ in range(300)]
    for largura in (1, 2, 5, 17):
        esperado = [max(valores[i : i + largura]) for i in range(len(valores) - largura + 1)]
        assert janela_deslizante_maximo(valores, largura) == esperado


@pytest.mark.parametrize("largura", [0, -1])
def test_janela_com_largura_invalida(largura: int) -> None:
    with pytest.raises(ValueError, match="positiva"):
        janela_deslizante_maximo([1, 2, 3], largura)
