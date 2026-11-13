# Vértice

O Vértice é o software de linha de comando que mantém o catálogo de uma livraria e monta a fatura de um cliente. O código-fonte está escrito em C++17 e usa apenas a biblioteca padrão.

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `docs/` | A especificação, o diagrama de classes e uma sessão de exemplo |
| `src/` | As classes `Author`, `Book`, `Customer` e `Invoice`, o módulo de pagamento e a `main`, com os cabeçalhos em `src/include` |
| `tests/unit/` | Os testes de unidade |
| `tests/dast/` | Os casos hostis usados no DAST |
| `.semgrep/` | As regras de SAST mantidas pela equipe |
| `.github/workflows/ci.yml` | O pipeline de integração contínua |
| `Makefile` | A construção e as verificações |

## Construção e execução

```sh
make
build/vertice < docs/sample-session.txt
```

Os comandos aceitos e as regras de negócio estão em [docs/specification.md](docs/specification.md), e o diagrama de classes, em [docs/class-diagram.md](docs/class-diagram.md).

## Testes

O comando `make` também constrói os testes em `build/tests`. Sem argumentos, esse binário executa todos os testes, com `--list` ele lista os nomes, e com um nome ele executa apenas aquele teste.

## Verificações

O `Makefile` oferece um alvo para cada verificação de segurança.

| Alvo | Verificação | Requisito |
|---|---|---|
| `make sast` | SAST com o Semgrep e as regras da pasta `.semgrep` | `pipx install semgrep==1.182.1` |
| `make sanitizers` | Análise dinâmica com os testes compilados com ASan e UBSan, cada teste num processo próprio | `g++` |
| `make valgrind` | Análise dinâmica com os testes executados sob o Valgrind, cada teste num processo próprio | `sudo apt-get install valgrind` |
| `make dast` | DAST com os casos hostis contra o binário `build/vertice` | `python3` |

Em kernels Linux recentes, o ASan pode falhar ao iniciar com a mensagem `AddressSanitizer:DEADLYSIGNAL`, pois o kernel sorteia endereços com mais bits do que ele suporta. Nesse caso, execute `sudo sysctl -w vm.mmap_rnd_bits=28` antes do `make sanitizers`.

## Pipeline

O arquivo `.github/workflows/ci.yml` é executado a cada push na `develop` e nas branches `feature/`, e a cada pull request para a `develop`.
