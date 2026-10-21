# algoritmos

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-C9A84C)
![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

**[English below](#english)**

Estruturas de dados e algoritmos clássicos **implementados do zero em Python**, cada um com testes e com uma explicação em português: a ideia, a complexidade (Big-O) e quando usar no mundo real.

## Por que este projeto

Lógica de programação se aprende fazendo. Este repositório é ao mesmo tempo um caderno de estudo e material de referência para quem está aprendendo — cada tópico pode ser lido, executado e testado isoladamente.

## O que está a caminho

O projeto está sendo construído em entregas pequenas, cada uma com testes e CI. Acompanhe pelos commits e pull requests.

- [x] [Pilha, fila, deque e lista ligada](estruturas_lineares/)
- [ ] Árvore binária de busca e heap
- [ ] Tabela hash com tratamento de colisão
- [ ] Ordenações (bubble, insertion, merge, quick, heap, counting) com comparação de desempenho
- [ ] Busca binária e variações
- [ ] Grafos: BFS, DFS, Dijkstra e ordenação topológica
- [ ] Programação dinâmica: mochila, LCS e troco
- [ ] Backtracking: N-rainhas, sudoku e torre de Hanói

## Como rodar

Requer Python 3.12 ou mais novo. Não há dependências de execução: tudo é feito
do zero, só com a biblioteca padrão.

```bash
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\activate
pip install pytest ruff mypy

pytest                             # testes (inclui os exemplos das docstrings)
ruff check . && ruff format --check .
mypy .                             # tipagem estrita
```

Cada tópico fica em uma pasta própria, com o código, os testes e um README
explicando a ideia, a complexidade e quando usar.

## Tecnologias

Python 3.12 · pytest · ruff · mypy · GitHub Actions

## Autor

**Euller Pinheiro**, Diretor Técnico da [ESX Tecnologia](https://esxtecnologia.com) — desenvolvimento de sistemas, infraestrutura e TI gerenciada em São Paulo.

---

<a name="english"></a>
## English

Classic data structures and algorithms implemented from scratch in Python, each with tests and a Portuguese explanation of the idea, its Big-O complexity and when to use it. Work in progress — built in small, tested increments. Licensed under [MIT](LICENSE).
