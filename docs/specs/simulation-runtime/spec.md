# Runtime da simulação

- **Estado:** Implemented
- **Última atualização:** 2026-08-01

## Propósito

Definir inicialização, temporização determinística, separação entre domínio e
GUI e execução automatizada sem interface.

## Escopo

- Inicialização da aplicação Qt.
- Scheduler de passo fixo e tratamento do tempo transcorrido.
- API pública do núcleo.
- Cenários de integração headless.
- Ambiente e comandos suportados.

## Fora de escopo

- Equações específicas da planta e aparência da interface.
- Empacotamento dos assets para instalação fora da raiz.

## Requisitos funcionais

- **SR-RF-01:** `main()` deve criar `QApplication`, abrir `MainWindow` em
  1200 × 700 px e iniciar o event loop.
- **SR-RF-02:** A janela deve solicitar atualizações em intervalo nominal de
  16 ms.
- **SR-RF-03:** Cada atualização deve calcular o tempo transcorrido com
  `time.monotonic()`.
- **SR-RF-04:** Cada atualização deve ler entradas, avançar o modelo e atualizar
  a apresentação nesta ordem.
- **SR-RF-05:** O pacote `sim` deve expor `SimState` e `Simulator` sem depender
  de Qt.
- **SR-RF-06:** O núcleo deve avançar em passos fixos de 1 ms e acumular a
  fração restante entre chamadas.
- **SR-RF-07:** Após uma pausa longa do processo, o avanço deve limitar a
  recuperação a 100 ms e registrar o tempo descartado.
- **SR-RF-08:** O executor headless deve carregar cenários declarativos,
  registrar amostras e resumo em JSON e CSV e falhar quando uma asserção não
  for satisfeita.

## Requisitos não funcionais

- **SR-RNF-01:** O projeto deve suportar Python 3.12 ou superior.
- **SR-RNF-02:** Dependências devem estar declaradas em `pyproject.toml`.
- **SR-RNF-03:** O núcleo e os cenários headless devem ser executáveis somente
  com a biblioteca padrão.
- **SR-RNF-04:** A qualidade deve ser verificada em pushes e pull requests.
- **SR-RNF-05:** Cenários com a mesma configuração e semente devem produzir os
  mesmos resultados.

## Critérios de aceitação

### SR-CA-01: núcleo independente

- **Dado** Python 3.12 sem PySide6;
- **Quando** os testes de `sim` são executados;
- **Então** o núcleo deve importar e os testes devem passar.

### SR-CA-02: interface

- **Dado** o ambiente instalado e execução na raiz;
- **Quando** `python3 app.py` é executado;
- **Então** a janela deve abrir e atualizar continuamente.

### SR-CA-03: temporização

- **Dado** uma sequência de intervalos de GUI variáveis;
- **Quando** o simulador avança;
- **Então** o domínio deve usar passos de 1 ms e limitar recuperações longas a
  100 ms sem instabilidade numérica.

### SR-CA-04: qualidade

- **Dado** um push ou pull request;
- **Quando** o workflow `Quality` executa;
- **Então** documentação, testes unitários, cenários headless e sintaxe devem
  ser validados.

## Limitações vigentes

- Assets ainda usam caminhos relativos à raiz do repositório.
- O workflow não executa testes gráficos.
- Os cenários headless validam o modelo, mas não a renderização Qt.

## Evidências

- **Código:** `app.py`, `sim/`, `tools/run_scenarios.py`, `pyproject.toml` e
  `.github/workflows/quality.yml`.
- **Testes:** 42 testes unitários e oito cenários de integração headless.
- **Validação manual:** interface e entrega integral do item 2 validadas pelo
  mantenedor em 2026-08-01.
