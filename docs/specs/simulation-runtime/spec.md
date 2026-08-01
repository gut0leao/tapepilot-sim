# Runtime da simulação

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir inicialização, temporização e separação mínima entre domínio e GUI.

## Escopo

- Inicialização da aplicação Qt.
- Timer e cálculo do tempo transcorrido.
- API pública do núcleo.
- Ambiente e comandos suportados.

## Fora de escopo

- Equações do modelo e aparência da interface.
- Empacotamento dos assets para instalação fora da raiz.

## Requisitos funcionais

- **SR-RF-01:** `main()` deve criar `QApplication`, abrir `MainWindow` em
  1200 × 700 px e iniciar o event loop.
- **SR-RF-02:** A janela deve solicitar ticks em intervalo nominal de 16 ms.
- **SR-RF-03:** Cada tick deve calcular `dt` com `time.monotonic()`.
- **SR-RF-04:** Cada tick deve ler entradas, executar o modelo e atualizar a
  apresentação nesta ordem.
- **SR-RF-05:** O pacote `sim` deve expor `SimState` e `Simulator` sem depender
  de Qt.

## Requisitos não funcionais

- **SR-RNF-01:** O projeto deve suportar Python 3.12 ou superior.
- **SR-RNF-02:** Dependências devem estar declaradas em `pyproject.toml`.
- **SR-RNF-03:** O núcleo deve ser testável somente com a biblioteca padrão.
- **SR-RNF-04:** A qualidade deve ser verificada em pushes e pull requests.

## Critérios de aceitação

### SR-CA-01: núcleo independente

- **Dado** Python 3.12 sem PySide6;
- **Quando** os testes de `sim` são executados;
- **Então** o núcleo deve importar e os testes devem passar.

### SR-CA-02: interface

- **Dado** o ambiente instalado e execução na raiz;
- **Quando** `python3 app.py` é executado;
- **Então** a janela deve abrir e atualizar continuamente.

### SR-CA-03: qualidade

- **Dado** um push ou pull request;
- **Quando** o workflow `Quality` executa;
- **Então** documentação, testes e sintaxe devem ser validados.

## Limitações vigentes

- A taxa da simulação está acoplada à atualização da GUI.
- `dt` não é validado.
- Assets usam caminhos relativos à raiz do repositório.
- O workflow não executa testes gráficos.

## Evidências

- **Código:** `app.py`, `sim/`, `pyproject.toml`,
  `.github/workflows/quality.yml`.
- **Testes:** seis testes de caracterização passam sem Qt.
- **Validação manual:** interface validada em 2026-07-31; workflow validado no
  GitHub Actions após o push.

