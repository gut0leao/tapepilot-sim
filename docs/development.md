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
python3 -m unittest discover -v
python3 -m py_compile app.py sim/*.py tests/*.py tools/*.py
```

O pytest faz parte do extra `dev` instalado por `pip install -e '.[dev]'`. Com
esse extra instalado, também é possível usar:

```bash
python3 -m pytest
```

Os testes do domínio não exigem a criação de uma janela Qt.

### Cobertura de caracterização atual

Os testes registram o comportamento existente de:

- setpoint dos cinco modos;
- saturação positiva e negativa do PWM;
- resposta de primeira ordem;
- efeito do atrito sobre RPM e tensão;
- convergência para zero em `STOP`;
- avanço dos três ângulos visuais.

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
