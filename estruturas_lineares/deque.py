"""Deque (double-ended queue): inserir e remover nas duas pontas em O(1).

Implementação com **buffer circular**: um array de tamanho fixo em que o
índice "dá a volta" no final, como um relógio. Guardamos onde está o
primeiro elemento (``_inicio``) e quantos existem (``_tamanho``); a posição
do i-ésimo elemento é ``(_inicio + i) % capacidade``.

- Colocar à esquerda é só recuar ``_inicio`` uma posição (com a volta).
- Colocar à direita é escrever em ``(_inicio + _tamanho) % capacidade``.
- Quando o array enche, criamos outro com o dobro do tamanho e copiamos
  os elementos já "desenrolados". Como a cópia acontece cada vez mais
  raramente, o custo amortizado continua O(1).
- Quando sobra muito espaço (ocupação de 1/4), o array encolhe pela
  metade, para não reter memória depois de um pico.

Bônus do buffer circular: acesso por índice ``deque[i]`` em O(1), algo que
uma lista ligada não oferece.
"""

from collections.abc import Iterable, Iterator
from typing import cast

from estruturas_lineares.erros import EstruturaVaziaError

CAPACIDADE_MINIMA = 8


class Deque[T]:
    """Fila de duas pontas sobre buffer circular redimensionável."""

    __slots__ = ("_buffer", "_inicio", "_tamanho")

    def __init__(self, itens: Iterable[T] = ()) -> None:
        """Cria o deque; os itens iniciais entram pela direita, na ordem dada."""
        self._buffer: list[T | None] = [None] * CAPACIDADE_MINIMA
        self._inicio = 0
        self._tamanho = 0
        for item in itens:
            self.adicionar_direita(item)

    # ----- inserção -------------------------------------------------------

    def adicionar_direita(self, item: T) -> None:
        """Insere ``item`` no fim. O(1) amortizado."""
        self._garantir_espaco()
        self._buffer[self._posicao(self._tamanho)] = item
        self._tamanho += 1

    def adicionar_esquerda(self, item: T) -> None:
        """Insere ``item`` no início. O(1) amortizado."""
        self._garantir_espaco()
        self._inicio = (self._inicio - 1) % len(self._buffer)
        self._buffer[self._inicio] = item
        self._tamanho += 1

    # ----- remoção --------------------------------------------------------

    def remover_direita(self) -> T:
        """Remove e devolve o último elemento. O(1) amortizado.

        Raises:
            EstruturaVaziaError: se o deque estiver vazio.
        """
        if self._tamanho == 0:
            raise EstruturaVaziaError("remover_direita de um deque vazio")
        posicao = self._posicao(self._tamanho - 1)
        item = cast(T, self._buffer[posicao])
        self._buffer[posicao] = None  # solta a referência para o coletor de lixo
        self._tamanho -= 1
        self._talvez_encolher()
        return item

    def remover_esquerda(self) -> T:
        """Remove e devolve o primeiro elemento. O(1) amortizado.

        Raises:
            EstruturaVaziaError: se o deque estiver vazio.
        """
        if self._tamanho == 0:
            raise EstruturaVaziaError("remover_esquerda de um deque vazio")
        item = cast(T, self._buffer[self._inicio])
        self._buffer[self._inicio] = None
        self._inicio = (self._inicio + 1) % len(self._buffer)
        self._tamanho -= 1
        self._talvez_encolher()
        return item

    # ----- consulta -------------------------------------------------------

    def primeiro(self) -> T:
        """Devolve o primeiro elemento sem removê-lo. O(1)."""
        if self._tamanho == 0:
            raise EstruturaVaziaError("primeiro de um deque vazio")
        return self[0]

    def ultimo(self) -> T:
        """Devolve o último elemento sem removê-lo. O(1)."""
        if self._tamanho == 0:
            raise EstruturaVaziaError("ultimo de um deque vazio")
        return self[-1]

    def __getitem__(self, indice: int) -> T:
        """Acesso por índice em O(1); aceita índices negativos como a ``list``."""
        if indice < 0:
            indice += self._tamanho
        if not 0 <= indice < self._tamanho:
            raise IndexError("índice fora do deque")
        return cast(T, self._buffer[self._posicao(indice)])

    def vazio(self) -> bool:
        """Indica se o deque não tem elementos. O(1)."""
        return self._tamanho == 0

    def __len__(self) -> int:
        return self._tamanho

    def __bool__(self) -> bool:
        return self._tamanho > 0

    def __iter__(self) -> Iterator[T]:
        """Percorre da esquerda para a direita."""
        for i in range(self._tamanho):
            yield cast(T, self._buffer[self._posicao(i)])

    def __repr__(self) -> str:
        return f"Deque({list(self)!r})"

    @property
    def capacidade(self) -> int:
        """Tamanho atual do buffer interno (útil para estudar o redimensionamento)."""
        return len(self._buffer)

    # ----- detalhes internos ---------------------------------------------

    def _posicao(self, deslocamento: int) -> int:
        """Converte a posição lógica (0 = primeiro) na posição física do buffer."""
        return (self._inicio + deslocamento) % len(self._buffer)

    def _garantir_espaco(self) -> None:
        if self._tamanho == len(self._buffer):
            self._redimensionar(len(self._buffer) * 2)

    def _talvez_encolher(self) -> None:
        # Encolhe em 1/4 (e não em 1/2) para evitar o "vai e vem": se
        # encolhêssemos na metade, alternar inserir/remover bem na fronteira
        # faria o array dobrar e encolher a cada operação.
        capacidade = len(self._buffer)
        if capacidade > CAPACIDADE_MINIMA and self._tamanho <= capacidade // 4:
            self._redimensionar(max(CAPACIDADE_MINIMA, capacidade // 2))

    def _redimensionar(self, nova_capacidade: int) -> None:
        novo: list[T | None] = [None] * nova_capacidade
        for i in range(self._tamanho):
            novo[i] = self._buffer[self._posicao(i)]
        self._buffer = novo
        self._inicio = 0


def janela_deslizante_maximo(valores: list[int], largura: int) -> list[int]:
    """Máximo de cada janela de ``largura`` elementos consecutivos, em O(n).

    Uso clássico de deque: guardamos índices em ordem decrescente de valor.
    Quem sai da janela é removido pela esquerda; quem é menor que o novo
    valor nunca mais será máximo e é removido pela direita.

    >>> janela_deslizante_maximo([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
    """
    if largura <= 0:
        raise ValueError("a largura da janela deve ser positiva")
    candidatos: Deque[int] = Deque()
    maximos: list[int] = []
    for i, valor in enumerate(valores):
        if candidatos and candidatos.primeiro() <= i - largura:
            candidatos.remover_esquerda()
        while candidatos and valores[candidatos.ultimo()] <= valor:
            candidatos.remover_direita()
        candidatos.adicionar_direita(i)
        if i >= largura - 1:
            maximos.append(valores[candidatos.primeiro()])
    return maximos
