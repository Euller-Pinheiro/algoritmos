# Estruturas lineares: pilha, fila, deque e lista ligada

**[English below](#english)**

Estruturas lineares guardam elementos em sequência. O que muda entre elas é
**por onde os elementos entram e saem** — e é essa regra que decide qual usar.

| Estrutura | Regra | Arquivo | Implementação |
|---|---|---|---|
| Pilha | último a entrar, primeiro a sair (LIFO) | [`pilha.py`](pilha.py) | array dinâmico (`list`) |
| Fila | primeiro a entrar, primeiro a sair (FIFO) | [`fila.py`](fila.py) | nós encadeados |
| Deque | entra e sai pelas duas pontas | [`deque.py`](deque.py) | buffer circular |
| Lista ligada | sequência de nós, cada um aponta para o próximo | [`lista_ligada.py`](lista_ligada.py) | nós encadeados |

Cada uma foi implementada de um jeito diferente de propósito: assim dá para
comparar **array** e **encadeamento**, as duas formas básicas de organizar dados
na memória.

## Complexidade (Big-O)

| Operação | Pilha | Fila | Deque | Lista ligada |
|---|---|---|---|---|
| Inserir no início | — | — | O(1)* | O(1) |
| Inserir no fim | O(1)* | O(1) | O(1)* | O(1) (com ponteiro de cauda) |
| Remover do início | — | O(1) | O(1)* | O(1) |
| Remover do fim | O(1) | — | O(1)* | **O(n)** |
| Acessar o i-ésimo | — | — | O(1) | **O(n)** |
| Buscar um valor | — | — | O(n) | O(n) |

\* amortizado: quase sempre é O(1), mas de vez em quando o array cresce e
copia tudo. Como ele **dobra** de tamanho, essas cópias ficam cada vez mais
raras e o custo médio por operação continua constante.

## Pilha

Pense numa pilha de pratos: você só mexe no de cima. Em Python, uma `list`
usada só pelo final (`append`/`pop`) já é uma ótima pilha; a classe `Pilha`
deixa a intenção explícita e impede o uso "errado" (tirar do meio).

**Quando usar:** desfazer/refazer em editores, pilha de chamadas de função,
navegação "voltar" do navegador, avaliar expressões, percorrer árvores e grafos
em profundidade (DFS) sem recursão.

**Exemplo incluído:** `parenteses_balanceados("f(a[1], {b: 2})")` — cada abertura
é empilhada e cada fechamento precisa casar com o topo.

## Fila

Pense na fila do banco. O erro mais comum em Python é implementar fila com
`list.pop(0)`: remover o primeiro elemento de um array desloca **todos** os
outros, então cada saída custa O(n). A `Fila` deste projeto usa nós
encadeados com ponteiros para o início e para o fim, e as duas operações são
O(1) no pior caso.

**Quando usar:** filas de tarefas e mensagens, impressão, atendimento por ordem
de chegada, busca em largura (BFS) em grafos.

**Borda que pega muita gente:** ao remover o último elemento, o ponteiro de
**fim** também precisa virar `None`. Se não virar, o próximo `enfileirar`
pendura o nó novo num nó que já saiu da fila e o dado se perde. Há um teste só
para isso (`test_reutilizar_depois_de_esvaziar`).

## Deque

O deque guarda os itens num **buffer circular**: um array em que o índice "dá a
volta" no final, como os ponteiros de um relógio. A posição física do i-ésimo
elemento é `(inicio + i) % capacidade`.

```
capacidade 8, inicio = 6, tamanho = 4

índice físico:  0    1    2    3    4    5    6    7
buffer:       [ c ][ d ][   ][   ][   ][   ][ a ][ b ]
                                            ↑ inicio
ordem lógica: a, b, c, d
```

- Quando enche, o buffer **dobra** e os itens são copiados já "desenrolados".
- Quando a ocupação cai para **1/4**, o buffer encolhe pela metade. Por que 1/4
  e não 1/2? Se encolhesse na metade, alternar inserir/remover bem na fronteira
  faria o array dobrar e encolher a cada operação.

**Quando usar:** histórico com tamanho limitado, algoritmos de janela
deslizante, BFS 0-1, fila que às vezes precisa "furar" pela frente. No dia a dia
em Python, use `collections.deque`; aqui o objetivo é entender como ela funciona
por dentro (o teste `test_comportamento_igual_ao_deque_nativo` compara as duas
com 5.000 operações aleatórias).

**Exemplo incluído:** `janela_deslizante_maximo([1, 3, -1, -3, 5, 3, 6, 7], 3)`
devolve o máximo de cada janela em O(n), em vez de O(n·k) da força bruta.

## Lista ligada

Cada elemento fica num nó com o valor e a referência para o próximo. Não há
array: inserir ou remover no início é só trocar uma referência. Em troca, para
chegar ao 500º elemento é preciso caminhar 500 nós.

**Quando usar:** quando o programa insere e remove muito nas pontas ou no meio
de uma sequência que ele já está percorrendo, e quase nunca acessa por índice.
Ela é a base de outras estruturas (filas, tabelas hash com encadeamento, listas
de adjacência de grafos). Na prática, em Python, a `list` costuma ganhar pelo
uso de cache da CPU — mas entender ponteiros é indispensável.

**Técnicas incluídas:**

- `inverter()` — inverte a lista só trocando ponteiros, sem memória extra.
- `meio()` — dois ponteiros, um lento e um rápido: quando o rápido chega ao fim,
  o lento está no meio. A mesma ideia detecta ciclos (algoritmo de Floyd).

## Como usar

```python
from estruturas_lineares import Deque, Fila, ListaLigada, Pilha

pilha = Pilha([1, 2, 3])
pilha.desempilhar()  # 3

fila = Fila(["ana", "bia"])
fila.desenfileirar()  # "ana"

deque = Deque([2, 3])
deque.adicionar_esquerda(1)  # [1, 2, 3]

lista = ListaLigada("abc")
lista.inverter()  # c -> b -> a
```

Todas levantam `EstruturaVaziaError` (uma subclasse de `IndexError`) ao ler ou
remover de uma estrutura vazia.

## Exercícios sugeridos

1. Implemente uma fila usando **duas pilhas** e explique por que o custo
   amortizado continua O(1).
2. Transforme a `ListaLigada` em duplamente ligada e implemente `remover_fim` em O(1).
3. Detecte se uma lista ligada tem ciclo usando os ponteiros lento e rápido.
4. Use a `Pilha` para converter uma expressão infixa (`3 + 4 * 2`) em pós-fixa.

---

<a name="english"></a>
## English

Linear data structures implemented from scratch: a **stack** (on a dynamic
array), a **queue** (linked nodes with head and tail pointers, O(1) dequeue
instead of `list.pop(0)`), a **deque** (resizable circular buffer that doubles
when full and halves at 1/4 occupancy, with O(1) indexing) and a **singly linked
list** (with in-place reversal and the slow/fast pointer technique). Each file
documents the Big-O of every operation, and the tests cover edge cases such as
resetting the tail pointer when the structure becomes empty.
