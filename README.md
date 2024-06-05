# Desafio Cartesi Code Challenge

Solução do desafio proposto no [Cartesi Masterclass Workshop](https://github.com/henriquemarlon/cartesi-code-challenge-1) da Cartesi, no Inteli.

## **A lógica do dapp.py**

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

## Como fizemos?
- Antes de mexer com a Cartesi, resolvemos apenas o problema da arvore binaria em um programa python separado.
- Com o repositório clonado, entramos no dir do dapp e buildamos com `cartesi build`.
- Rodamos com `cartesi run`.
- Damos um inspect no url `http://localhost:8080/inspect/` e o payload é `Blue`
- Enviamos um **advance** com a Cartesi Cli:
  ```
  cartesi send generic \
    --dapp=0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e \
    --chain-id=31337 \
    --rpc-url=http://127.0.0.1:8545 \
    --mnemonic-passphrase='test test test test test test test test test test test junk' \
    --input='20'
  ```
- Após isso, os inspects voltam com a resposta correta, *red*:
![image](https://github.com/paulo-evangelista/cartesi-challenge/assets/99093520/b14344e0-f5e6-4ff3-97ba-d2f3e2e2f281)
