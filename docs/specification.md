# Especificação do Vértice

## Regras de negócio

- Um autor tem identificador, nome com até 47 bytes e gênero, que vale `M` ou `F`.
- Um livro tem identificador, título, autor e preço não negativo. O título é guardado com até 63 bytes, e um título mais longo é truncado.
- Um cliente tem identificador, nome e desconto, um percentual inteiro de 0 a 100.
- A fatura pertence a um cliente e contém no máximo 10 livros diferentes. Cada livro entra na fatura uma única vez e com quantidade positiva.
- O total da fatura é a soma do preço de cada livro multiplicado pela sua quantidade, e o total com desconto aplica sobre ele o percentual do cliente.
- O pagamento envia o total com desconto ao gateway de pagamentos, que só autoriza valores positivos.

## Comandos

O programa lê um comando por linha da entrada padrão e responde a cada um com `ok`, com o resultado ou com uma mensagem que começa com `Error`. Linhas vazias e linhas que começam com `#` são ignoradas.

| Comando | Efeito |
|---|---|
| `customer <id> <discount> <name>` | Abre a fatura do cliente |
| `author <id> <M or F> <name>` | Cadastra um autor |
| `book <id> <author_id> <price> <title>` | Cadastra um livro no catálogo |
| `add <book_id> <quantity>` | Acrescenta um livro à fatura |
| `remove <book_id>` | Remove um livro da fatura |
| `invoice` | Mostra a fatura, com o total já com desconto |
| `pay` | Paga o total da fatura com desconto |

## Sessão de exemplo

O comando `build/vertice < docs/sample-session.txt` produz a seguinte saída.

```
ok
ok
ok
ok
ok
ok
Invoice[id = 1, Customer[id = 7, name = Ana Souza, discount = 10], total = 94.32]
Payment of 94.32 authorized
```
