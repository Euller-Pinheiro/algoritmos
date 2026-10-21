"""Lista ligada simples (singly linked list).

Cada elemento vive em um nó que conhece apenas o próximo. Não há array por
trás: inserir ou remover no início é só trocar uma referência (O(1)), mas
chegar ao k-ésimo elemento exige caminhar k nós (O(n)).

Guardamos também o último nó, para que ``adicionar_fim`` seja O(1). Remover
do fim, porém, continua O(n): para isso seria preciso conhecer o penúltimo
nó, o que só uma lista **duplamente** ligada oferece em O(1).
"""

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from estruturas_lineares.erros import EstruturaVaziaError


@dataclass(slots=True)
class No[T]:
    """Nó da lista: o valor e a referência para o próximo nó (ou ``None``)."""

    valor: T
    proximo: "No[T] | None" = None


class ListaLigada[T]:
    """Lista ligada simples com ponteiros para a cabeça e para a cauda."""

    __slots__ = ("_cabeca", "_cauda", "_tamanho")

    def __init__(self, itens: Iterable[T] = ()) -> None:
        """Cria a lista; os itens iniciais são adicionados ao fim, na ordem dada."""
        self._cabeca: No[T] | None = None
        self._cauda: No[T] | None = None
        self._tamanho = 0
        for item in itens:
            self.adicionar_fim(item)

    # ----- inserção -------------------------------------------------------

    def adicionar_inicio(self, valor: T) -> None:
        """Insere ``valor`` antes do primeiro elemento. O(1)."""
        self._cabeca = No(valor, self._cabeca)
        if self._cauda is None:
            self._cauda = self._cabeca
        self._tamanho += 1

    def adicionar_fim(self, valor: T) -> None:
        """Insere ``valor`` depois do último elemento. O(1) graças à cauda."""
        no = No(valor)
        if self._cauda is None:
            self._cabeca = no
        else:
            self._cauda.proximo = no
        self._cauda = no
        self._tamanho += 1

    def inserir(self, indice: int, valor: T) -> None:
        """Insere ``valor`` na posição ``indice`` (0 ≤ indice ≤ tamanho). O(n).

        Raises:
            IndexError: se o índice estiver fora do intervalo.
        """
        if not 0 <= indice <= self._tamanho:
            raise IndexError("índice de inserção fora da lista")
        if indice == 0:
            self.adicionar_inicio(valor)
        elif indice == self._tamanho:
            self.adicionar_fim(valor)
        else:
            anterior = self._no_em(indice - 1)
            anterior.proximo = No(valor, anterior.proximo)
            self._tamanho += 1

    # ----- remoção --------------------------------------------------------

    def remover_inicio(self) -> T:
        """Remove e devolve o primeiro elemento. O(1).

        Raises:
            EstruturaVaziaError: se a lista estiver vazia.
        """
        if self._cabeca is None:
            raise EstruturaVaziaError("remover_inicio de uma lista vazia")
        no = self._cabeca
        self._cabeca = no.proximo
        if self._cabeca is None:
            self._cauda = None
        self._tamanho -= 1
        return no.valor

    def remover(self, valor: T) -> None:
        """Remove a primeira ocorrência de ``valor``. O(n).

        Raises:
            ValueError: se o valor não estiver na lista (igual a ``list.remove``).
        """
        anterior: No[T] | None = None
        atual = self._cabeca
        while atual is not None and atual.valor != valor:
            anterior, atual = atual, atual.proximo
        if atual is None:
            raise ValueError(f"{valor!r} não está na lista")
        if anterior is None:
            self._cabeca = atual.proximo
        else:
            anterior.proximo = atual.proximo
        if atual is self._cauda:
            self._cauda = anterior
        self._tamanho -= 1

    # ----- consulta -------------------------------------------------------

    def primeiro(self) -> T:
        """Devolve o primeiro elemento. O(1)."""
        if self._cabeca is None:
            raise EstruturaVaziaError("primeiro de uma lista vazia")
        return self._cabeca.valor

    def ultimo(self) -> T:
        """Devolve o último elemento. O(1) graças à cauda."""
        if self._cauda is None:
            raise EstruturaVaziaError("ultimo de uma lista vazia")
        return self._cauda.valor

    def buscar(self, condicao: Callable[[T], bool]) -> T | None:
        """Devolve o primeiro elemento que satisfaz ``condicao``, ou ``None``. O(n)."""
        for valor in self:
            if condicao(valor):
                return valor
        return None

    def indice(self, valor: T) -> int:
        """Posição da primeira ocorrência de ``valor``. O(n).

        Raises:
            ValueError: se o valor não estiver na lista.
        """
        for posicao, atual in enumerate(self):
            if atual == valor:
                return posicao
        raise ValueError(f"{valor!r} não está na lista")

    def __getitem__(self, indice: int) -> T:
        """Acesso por índice em O(n): é preciso caminhar até o nó."""
        if indice < 0:
            indice += self._tamanho
        if not 0 <= indice < self._tamanho:
            raise IndexError("índice fora da lista")
        return self._no_em(indice).valor

    def __contains__(self, valor: object) -> bool:
        return any(atual == valor for atual in self)

    # ----- transformação --------------------------------------------------

    def inverter(self) -> None:
        """Inverte a lista no lugar, só trocando ponteiros. O(n) tempo, O(1) memória.

        >>> lista = ListaLigada([1, 2, 3])
        >>> lista.inverter()
        >>> list(lista)
        [3, 2, 1]
        """
        anterior: No[T] | None = None
        atual = self._cabeca
        self._cauda = atual
        while atual is not None:
            atual.proximo, anterior, atual = anterior, atual, atual.proximo
        self._cabeca = anterior

    def meio(self) -> T:
        """Elemento do meio pela técnica de dois ponteiros (lento e rápido). O(n).

        O ponteiro rápido anda dois nós por vez; quando ele chega ao fim, o
        lento está no meio. Com quantidade par, devolve o segundo do meio.
        Não usa ``_tamanho`` de propósito: a técnica é útil quando o tamanho
        não é conhecido.
        """
        if self._cabeca is None:
            raise EstruturaVaziaError("meio de uma lista vazia")
        lento = self._cabeca
        rapido: No[T] | None = self._cabeca
        while rapido is not None and rapido.proximo is not None:
            # O lento nunca passa do rápido, então o próximo dele existe.
            lento = lento.proximo  # type: ignore[assignment]
            rapido = rapido.proximo.proximo
        return lento.valor

    # ----- protocolo de coleção ------------------------------------------

    def vazia(self) -> bool:
        """Indica se a lista não tem elementos. O(1)."""
        return self._tamanho == 0

    def __len__(self) -> int:
        return self._tamanho

    def __bool__(self) -> bool:
        return self._tamanho > 0

    def __iter__(self) -> Iterator[T]:
        no = self._cabeca
        while no is not None:
            yield no.valor
            no = no.proximo

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ListaLigada):
            return NotImplemented
        return len(self) == len(outro) and all(a == b for a, b in zip(self, outro, strict=True))

    __hash__ = None  # type: ignore[assignment]  # mutável, como a list

    def __repr__(self) -> str:
        return f"ListaLigada({list(self)!r})"

    def _no_em(self, indice: int) -> No[T]:
        no = self._cabeca
        for _ in range(indice):
            assert no is not None
            no = no.proximo
        assert no is not None
        return no
