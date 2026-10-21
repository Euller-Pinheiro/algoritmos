"""Pilha (stack): o último a entrar é o primeiro a sair (LIFO).

Implementação sobre um array dinâmico (a ``list`` do Python), usando apenas o
final da lista. Inserir e remover no final de um array dinâmico custa O(1)
amortizado: de vez em quando o array cresce e copia tudo, mas esse custo,
dividido por todas as inserções, dá uma constante.
"""

from collections.abc import Iterable, Iterator

from estruturas_lineares.erros import EstruturaVaziaError


class Pilha[T]:
    """Pilha LIFO com ``empilhar``, ``desempilhar`` e ``topo`` em O(1)."""

    __slots__ = ("_itens",)

    def __init__(self, itens: Iterable[T] = ()) -> None:
        """Cria a pilha; os itens iniciais são empilhados na ordem dada."""
        self._itens: list[T] = list(itens)

    def empilhar(self, item: T) -> None:
        """Coloca ``item`` no topo. O(1) amortizado."""
        self._itens.append(item)

    def desempilhar(self) -> T:
        """Remove e devolve o item do topo. O(1).

        Raises:
            EstruturaVaziaError: se a pilha estiver vazia.
        """
        if not self._itens:
            raise EstruturaVaziaError("desempilhar de uma pilha vazia")
        return self._itens.pop()

    def topo(self) -> T:
        """Devolve o item do topo sem removê-lo. O(1).

        Raises:
            EstruturaVaziaError: se a pilha estiver vazia.
        """
        if not self._itens:
            raise EstruturaVaziaError("topo de uma pilha vazia")
        return self._itens[-1]

    def vazia(self) -> bool:
        """Indica se a pilha não tem elementos. O(1)."""
        return not self._itens

    def limpar(self) -> None:
        """Remove todos os elementos."""
        self._itens.clear()

    def __len__(self) -> int:
        return len(self._itens)

    def __bool__(self) -> bool:
        return bool(self._itens)

    def __iter__(self) -> Iterator[T]:
        """Percorre do topo para a base (a ordem em que sairiam)."""
        return reversed(self._itens)

    def __repr__(self) -> str:
        return f"Pilha({self._itens!r})"


def parenteses_balanceados(texto: str) -> bool:
    """Verifica se ``()``, ``[]`` e ``{}`` estão abertos e fechados na ordem certa.

    É o exemplo clássico de uso de pilha: cada abertura é empilhada e cada
    fechamento precisa casar com o topo. Outros caracteres são ignorados.

    >>> parenteses_balanceados("f(a[1], {b: 2})")
    True
    >>> parenteses_balanceados("(]")
    False
    """
    pares = {")": "(", "]": "[", "}": "{"}
    abertos: Pilha[str] = Pilha()
    for caractere in texto:
        if caractere in "([{":
            abertos.empilhar(caractere)
        elif caractere in pares and (abertos.vazia() or abertos.desempilhar() != pares[caractere]):
            return False
    return abertos.vazia()
