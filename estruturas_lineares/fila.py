"""Fila (queue): o primeiro a entrar é o primeiro a sair (FIFO).

Por que não usar ``list.pop(0)``? Remover o primeiro elemento de um array
obriga a deslocar todos os outros uma posição para a esquerda: O(n). Em uma
fila com milhares de itens isso vira gargalo.

Aqui a fila é encadeada: cada nó aponta para o próximo, e guardamos
referências para o início (de onde sai) e para o fim (onde entra). Assim
``enfileirar`` e ``desenfileirar`` são O(1) no pior caso, sem cópias.
"""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from estruturas_lineares.erros import EstruturaVaziaError


@dataclass(slots=True)
class _No[T]:
    valor: T
    proximo: "_No[T] | None" = None


class Fila[T]:
    """Fila FIFO encadeada com ``enfileirar`` e ``desenfileirar`` em O(1)."""

    __slots__ = ("_fim", "_inicio", "_tamanho")

    def __init__(self, itens: Iterable[T] = ()) -> None:
        """Cria a fila; os itens iniciais entram na ordem dada."""
        self._inicio: _No[T] | None = None
        self._fim: _No[T] | None = None
        self._tamanho = 0
        for item in itens:
            self.enfileirar(item)

    def enfileirar(self, item: T) -> None:
        """Coloca ``item`` no fim da fila. O(1)."""
        no = _No(item)
        if self._fim is None:
            self._inicio = no
        else:
            self._fim.proximo = no
        self._fim = no
        self._tamanho += 1

    def desenfileirar(self) -> T:
        """Remove e devolve o item do início da fila. O(1).

        Raises:
            EstruturaVaziaError: se a fila estiver vazia.
        """
        if self._inicio is None:
            raise EstruturaVaziaError("desenfileirar de uma fila vazia")
        no = self._inicio
        self._inicio = no.proximo
        if self._inicio is None:
            # A fila esvaziou: o fim também precisa deixar de apontar para o nó removido.
            self._fim = None
        self._tamanho -= 1
        return no.valor

    def frente(self) -> T:
        """Devolve o próximo item a sair, sem removê-lo. O(1).

        Raises:
            EstruturaVaziaError: se a fila estiver vazia.
        """
        if self._inicio is None:
            raise EstruturaVaziaError("frente de uma fila vazia")
        return self._inicio.valor

    def vazia(self) -> bool:
        """Indica se a fila não tem elementos. O(1)."""
        return self._tamanho == 0

    def __len__(self) -> int:
        return self._tamanho

    def __bool__(self) -> bool:
        return self._tamanho > 0

    def __iter__(self) -> Iterator[T]:
        """Percorre do início para o fim (a ordem em que sairiam)."""
        no = self._inicio
        while no is not None:
            yield no.valor
            no = no.proximo

    def __repr__(self) -> str:
        return f"Fila({list(self)!r})"
