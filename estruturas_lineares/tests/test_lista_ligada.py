import pytest

from estruturas_lineares import EstruturaVaziaError
from estruturas_lineares.lista_ligada import ListaLigada


def test_lista_nova_esta_vazia() -> None:
    lista: ListaLigada[int] = ListaLigada()
    assert lista.vazia()
    assert len(lista) == 0
    assert list(lista) == []


def test_adicionar_no_inicio_e_no_fim() -> None:
    lista: ListaLigada[int] = ListaLigada()
    lista.adicionar_fim(2)
    lista.adicionar_inicio(1)
    lista.adicionar_fim(3)
    assert list(lista) == [1, 2, 3]
    assert lista.primeiro() == 1
    assert lista.ultimo() == 3


def test_adicionar_inicio_em_lista_vazia_atualiza_a_cauda() -> None:
    lista: ListaLigada[str] = ListaLigada()
    lista.adicionar_inicio("a")
    assert lista.ultimo() == "a"
    lista.adicionar_fim("b")
    assert list(lista) == ["a", "b"]


@pytest.mark.parametrize(
    ("indice", "esperado"),
    [(0, [9, 1, 2, 3]), (1, [1, 9, 2, 3]), (2, [1, 2, 9, 3]), (3, [1, 2, 3, 9])],
)
def test_inserir_em_posicao(indice: int, esperado: list[int]) -> None:
    lista = ListaLigada([1, 2, 3])
    lista.inserir(indice, 9)
    assert list(lista) == esperado
    assert len(lista) == 4
    assert lista.ultimo() == esperado[-1]


@pytest.mark.parametrize("indice", [-1, 4])
def test_inserir_fora_da_lista(indice: int) -> None:
    with pytest.raises(IndexError):
        ListaLigada([1, 2, 3]).inserir(indice, 9)


def test_remover_inicio() -> None:
    lista = ListaLigada([1, 2])
    assert lista.remover_inicio() == 1
    assert lista.remover_inicio() == 2
    assert lista.vazia()
    lista.adicionar_fim(3)  # a cauda precisa ter sido zerada
    assert list(lista) == [3]


@pytest.mark.parametrize("operacao", ["remover_inicio", "primeiro", "ultimo", "meio"])
def test_lista_vazia_levanta_erro(operacao: str) -> None:
    lista: ListaLigada[int] = ListaLigada()
    with pytest.raises(EstruturaVaziaError):
        getattr(lista, operacao)()


@pytest.mark.parametrize(
    ("valor", "esperado", "ultimo"),
    [(1, [2, 3, 2], 2), (2, [1, 3, 2], 2), (3, [1, 2, 2], 2)],
)
def test_remover_primeira_ocorrencia(valor: int, esperado: list[int], ultimo: int) -> None:
    lista = ListaLigada([1, 2, 3, 2])
    lista.remover(valor)
    assert list(lista) == esperado
    assert lista.ultimo() == ultimo


def test_remover_o_ultimo_atualiza_a_cauda() -> None:
    lista = ListaLigada([1, 2, 3])
    lista.remover(3)
    assert lista.ultimo() == 2
    lista.adicionar_fim(4)
    assert list(lista) == [1, 2, 4]


def test_remover_unico_elemento() -> None:
    lista = ListaLigada(["x"])
    lista.remover("x")
    assert lista.vazia()
    with pytest.raises(EstruturaVaziaError):
        lista.ultimo()


def test_remover_valor_ausente() -> None:
    with pytest.raises(ValueError, match="não está na lista"):
        ListaLigada([1, 2]).remover(5)


def test_indice_contains_e_getitem() -> None:
    lista = ListaLigada("abc")
    assert lista.indice("c") == 2
    assert "b" in lista
    assert "z" not in lista
    assert lista[0] == "a"
    assert lista[-1] == "c"
    with pytest.raises(IndexError):
        lista[3]
    with pytest.raises(ValueError, match="não está na lista"):
        lista.indice("z")


def test_buscar_por_condicao() -> None:
    lista = ListaLigada([3, 8, 10, 15])
    assert lista.buscar(lambda numero: numero % 2 == 0) == 8
    assert lista.buscar(lambda numero: numero > 100) is None


@pytest.mark.parametrize("itens", [[], [1], [1, 2], [1, 2, 3, 4, 5]])
def test_inverter(itens: list[int]) -> None:
    lista = ListaLigada(itens)
    lista.inverter()
    assert list(lista) == itens[::-1]
    assert len(lista) == len(itens)
    if itens:
        assert lista.primeiro() == itens[-1]
        assert lista.ultimo() == itens[0]
        lista.adicionar_fim(99)  # a cauda deve apontar para o antigo primeiro
        assert list(lista)[-1] == 99


@pytest.mark.parametrize(
    ("itens", "esperado"),
    [([1], 1), ([1, 2], 2), ([1, 2, 3], 2), ([1, 2, 3, 4], 3), ([1, 2, 3, 4, 5], 3)],
)
def test_meio(itens: list[int], esperado: int) -> None:
    assert ListaLigada(itens).meio() == esperado


def test_igualdade_e_repr() -> None:
    assert ListaLigada([1, 2]) == ListaLigada([1, 2])
    assert ListaLigada([1, 2]) != ListaLigada([1])
    assert ListaLigada([1, 2]) != [1, 2]
    assert repr(ListaLigada([1, 2])) == "ListaLigada([1, 2])"


def test_lista_nao_e_hashable() -> None:
    with pytest.raises(TypeError):
        hash(ListaLigada([1]))
