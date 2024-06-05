# Desafio Cartesi Code Challenge

Solução do desafio proposto no [Cartesi Masterclass Workshop](https://github.com/henriquemarlon/cartesi-code-challenge-1) da Cartesi, no Inteli.

### **Lógica de Verificação usando Árvore Binária**

A função `check_guess` é onde a busca binária acontece. Ela recebe um número (`guess`) e verifica se este número está na lista pré-definida. A lista é tratada como uma árvore binária, onde cada "divisão" do processo de busca reduz pela metade a área de busca:

```python
def check_guess(guess):
    array = [9, 15, 17, 19, 20, 23]
    l, r = 0, len(array) - 1
    found = False

    while r >= l:
        m = l + (r - l) // 2
        if array[m] == guess:
            found = True
            if m == 4:
                return State.RED
            break
        elif array[m] > guess:
            r = m - 1
        else:
            l = m + 1

    return State.RED
```

Nesta função, o código continua a busca até encontrar o valor ou exaurir as opções. O retorno para `State.RED` no caso de `m == 4` (quando o índice é igual a 4, o que corresponde ao número 20) indica uma condição especial para mudança de estado.

### Conclusão

A implementação utilizando árvore binária (busca binária) no array é um método eficiente para verificação, já que diminui significativamente o número de operações necessárias para encontrar um valor em uma lista ordenada, tornando o processo mais rápido e eficaz, especialmente útil neste contexto de verificar estados em tempo real.
