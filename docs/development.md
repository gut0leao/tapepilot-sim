# Desenvolvimento

## Ambiente de referência

- Ubuntu 24.04 ou WSL2 com WSLg;
- Python 3.12 ou superior;
- ambiente virtual criado com `venv`.

Outros ambientes podem funcionar, mas ainda não foram validados formalmente.

## Preparação

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e '.[dev]'
```

Dependências de sistema possivelmente necessárias no Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y \
  python3-venv python3-pip \
  libgl1 libegl1 libxkbcommon0 libxcb-cursor0 \
  libxrender1 libxext6 libx11-6
```

## Execução

Execute na raiz do repositório:

```bash
source .venv/bin/activate
python3 app.py
```

A raiz é necessária porque os SVGs são referenciados por caminhos relativos.

## Verificações disponíveis

Execute toda a validação local com:

```bash
python3 tools/check_docs.py
python3 tools/run_scenarios.py
python3 -m unittest discover -v
python3 -m py_compile app.py sim/*.py tests/*.py tools/*.py
```

O pytest faz parte do extra `dev` instalado por `pip install -e '.[dev]'`. Com
esse extra instalado, também é possível usar:

```bash
python3 -m pytest
```

Os testes do domínio não exigem a criação de uma janela Qt.

### Testes de integração headless por cenários

Os arquivos em `tests/scenarios/` descrevem sequências completas de transporte,
falhas e controle. Execute todos com:

```bash
python3 tools/run_scenarios.py --output test-results
```

Cada cenário gera uma série temporal CSV e um resumo JSON com métricas,
expectativas e resultado. `test-results/` é descartável e ignorado pelo Git.
Para executar somente um caso:

```bash
python3 tools/run_scenarios.py --scenario wow_tach_on
```

O processo retorna código diferente de zero se qualquer expectativa falhar.

O projeto distingue três níveis de teste:

- **unitários:** verificam isoladamente componentes como encoder, PID e métrica
  RMS;
- **integração headless por cenários:** integram transporte, planta, controle,
  encoder, perturbações, métricas, estado e tempo sem abrir a interface;
- **interface/end-to-end:** deverão exercitar Qt, eventos do usuário, SVGs e
  gráficos reais; ainda não estão implementados.

Os cenários headless não devem ser chamados de end-to-end porque não atravessam
a camada gráfica.

### Cobertura de caracterização atual

Os testes registram o comportamento existente de:

- setpoint dos cinco modos;
- saturação positiva e negativa do PWM;
- resposta de primeira ordem;
- efeito do atrito sobre RPM e tensão;
- convergência para zero em `STOP`;
- avanço dos três ângulos visuais.

Os testes de integração headless por cenários cobrem STOP prolongado, PLAY em
malha aberta, execução longa através de várias janelas RMS, comparação de wow
com Digital Tach OFF/ON, wow máximo, fallback de dropout e parada depois de
PLAY.

`wow_max_tach_on` é um teste de estresse com limite de regressão de `0,5%`; ele
não substitui o benchmark profissional de wow em `1%`, cujo limite permanece
`0,2%` e cuja meta é `0,1%`.

A interface Qt ainda não possui testes automatizados.

## Integração contínua

O workflow `.github/workflows/quality.yml` executa a verificação documental,
os testes de caracterização e a compilação dos módulos Python em pushes e pull
requests.

## Convenções

- Identificadores de código em inglês.
- Documentação do projeto em português.
- Uma responsabilidade principal por módulo.
- Novos comportamentos começam por proposta e delta aprovados.
- Decisões duradouras são registradas em ADRs.
- A documentação deve distinguir comportamento atual de intenção futura.

## Fluxo recomendado para mudanças

1. Classifique a mudança conforme `docs/changes/README.md`.
2. Crie proposta e delta quando houver mudança de comportamento.
3. Registre um ADR se houver uma decisão arquitetural duradoura.
4. Implemente tarefas pequenas e verificáveis.
5. Execute testes e validações estáticas.
6. Incorpore o delta às specs afetadas.
7. Atualize a documentação clássica e arquive a proposta.

Consulte também a [Definition of Done](specs/README.md#definition-of-done).

## Problemas comuns

### `ModuleNotFoundError`

Ative `.venv` e instale as dependências Python.

### A janela não abre no WSL

Confirme que a distribuição usa WSLg e instale as bibliotecas gráficas listadas
acima.

### Um SVG não aparece

Confira o nome do arquivo, o caminho usado no código, o `viewBox` e a escala do
`QGraphicsSvgItem`.
