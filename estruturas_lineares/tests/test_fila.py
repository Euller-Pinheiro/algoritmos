import pytest

from estruturas_lineares import EstruturaVaziaError
from estruturas_lineares.fila import Fila


def test_fila_nova_esta_vazia() -> None:
    fila: Fila[int] = Fila()
    assert fila.vazia()
    assert len(fila) == 0
    assert not fila


def test_primeiro_a_entrar_e_o_primeiro_a_sair() -> None:
    fila: Fila[str] = Fila()
    for pessoa in ("ana", "bia", "caio"):
        fila.enfileirar(pessoa)
    assert [fila.desenfileirar() for _ in range(3)] == ["ana", "bia", "caio"]
    assert fila.vazia()


def test_frente_nao_remove() -> None:
    fila = Fila([1, 2])
    assert fila.frente() == 1
    assert len(fila) == 2


def test_itens_iniciais_e_iteracao() -> None:
    fila = Fila(range(5))
    assert list(fila) == [0, 1, 2, 3, 4]
    assert len(fila) == 5


@pytest.mark.parametrize("operacao", ["desenfileirar", "frente"])
def test_fila_vazia_levanta_erro(operacao: str) -> None:
    fila: Fila[int] = Fila()
    with pytest.raises(EstruturaVaziaError):
        getattr(fila, operacao)()


def test_reutilizar_depois_de_esvaziar() -> None:
    # Borda clássica: ao esvaziar, o ponteiro de fim precisa ser zerado,
    # senão o próximo enfileirar se perde em um nó que não está mais na fila.
    fila = Fila([1])
    assert fila.desenfileirar() == 1
    fila.enfileirar(2)
    fila.enfileirar(3)
    assert list(fila) == [2, 3]
    assert fila.desenfileirar() == 2
    assert fila.frente() == 3


def test_intercalar_operacoes() -> None:
    fila: Fila[int] = Fila()
    saida = []
    for numero in range(100):
        fila.enfileirar(numero)
        if numero % 3 == 0:
            saida.append(fila.desenfileirar())
    saida.extend(fila.desenfileirar() for _ in range(len(fila)))
    assert saida == list(range(100))


def test_repr() -> None:
    assert repr(Fila("ab")) == "Fila(['a', 'b'])"
