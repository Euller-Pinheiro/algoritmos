"""Erros compartilhados pelas estruturas lineares."""


class EstruturaVaziaError(IndexError):
    """Operação de leitura ou remoção em uma estrutura sem elementos.

    Herda de ``IndexError`` para se comportar como as coleções nativas do Python
    (``[].pop()`` também levanta ``IndexError``), mas com um nome que deixa a
    intenção explícita no código de quem usa.
    """
