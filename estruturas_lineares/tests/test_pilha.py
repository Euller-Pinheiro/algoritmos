import pytest

from estruturas_lineares import EstruturaVaziaError
from estruturas_lineares.pilha import Pilha, parenteses_balanceados


def test_pilha_nova_esta_vazia() -> None:
    pilha: Pilha[int] = Pilha()
    assert pilha.vazia()
    assert len(pilha) == 0
    assert not pilha


def test_ultimo_a_entrar_e_o_primeiro_a_sair() -> None:
    pilha: Pilha[int] = Pilha()
    for numero in (1, 2, 3):
        pilha.empilhar(numero)
    assert [pilha.desempilhar() for _ in range(3)] == [3, 2, 1]
    assert pilha.vazia()


def test_topo_nao_remove() -> None:
    pilha = Pilha(["a", "b"])
    assert pilha.topo() == "b"
    assert len(pilha) == 2


def test_itens_iniciais_sao_empilhados_na_ordem() -> None:
    pilha = Pilha([1, 2, 3])
    assert pilha.topo() == 3
    assert list(pilha) == [3, 2, 1]


def test_iteracao_nao_altera_a_pilha() -> None:
    pilha = Pilha([1, 2])
    list(pilha)
    assert len(pilha) == 2


@pytest.mark.parametrize("operacao", ["desempilhar", "topo"])
def test_pilha_vazia_levanta_erro(operacao: str) -> None:
    pilha: Pilha[int] = Pilha()
    with pytest.raises(EstruturaVaziaError):
        getattr(pilha, operacao)()


def test_erro_de_pilha_vazia_e_um_index_error() -> None:
    with pytest.raises(IndexError):
        Pilha[int]().desempilhar()


def test_limpar() -> None:
    pilha = Pilha(range(10))
    pilha.limpar()
    assert pilha.vazia()


def test_muitos_elementos() -> None:
    pilha: Pilha[int] = Pilha()
    for numero in range(10_000):
        pilha.empilhar(numero)
    assert pilha.desempilhar() == 9_999
    assert len(pilha) == 9_999


def test_repr() -> None:
    assert repr(Pilha([1, 2])) == "Pilha([1, 2])"


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("", True),
        ("sem delimitadores", True),
        ("()", True),
        ("([]{})", True),
        ("f(a[1], {b: 2})", True),
        ("(", False),
        (")", False),
        ("(]", False),
        ("([)]", False),
        ("(()", False),
        ("())", False),
    ],
)
def test_parenteses_balanceados(texto: str, esperado: bool) -> None:
    assert parenteses_balanceados(texto) is esperado
