# TapePilot Simulator

O TapePilot é um simulador visual e interativo de mecanismos de transporte de
fita. O projeto serve como bancada experimental para estudar controle de
velocidade, resposta mecânica e injeção de falhas antes de levar a lógica para
hardware embarcado.

> **Estado:** protótipo experimental. O modelo atual demonstra o ciclo de
> controle e a interface; ele ainda não representa com precisão um mecanismo
> real.

## O que já funciona

- Controles `PLAY`, `STOP`, `PAUSE`, `FF` e `REW`;
- modelo simplificado de velocidade de primeira ordem;
- controlador proporcional;
- animação em SVG das bobinas e do capstan;
- injeção de atrito e jitter por sliders;
- gráficos de RPM, PWM, erro e tensão simulada.

## Limitações principais

- `REW` ainda usa velocidade positiva, igual a `FF`;
- o jitter afeta a animação, mas ainda não fecha a malha de controle;
- a tensão não possui unidade física nem realimenta o modelo;
- controlador, planta, encoder e falhas ainda não são componentes separados;
- a taxa da simulação ainda acompanha a atualização da interface.

## Requisitos

- Python 3.12 ou superior;
- PySide6;
- pyqtgraph.

## Executando

Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
python3 app.py
```

Os assets são carregados por caminhos relativos. Por isso, execute o comando na
raiz do projeto.

No Ubuntu ou WSL, caso o Qt reclame de bibliotecas gráficas:

```bash
sudo apt update
sudo apt install -y \
  python3-venv python3-pip \
  libgl1 libegl1 libxkbcommon0 libxcb-cursor0 \
  libxrender1 libxext6 libx11-6
```

## Estrutura atual

```text
tapepilot-sim/
├── .github/workflows/
├── app.py
├── assets/
│   └── svg/
├── docs/
│   ├── decisions/
│   └── specs/
├── sim/
├── tests/
├── tools/
├── pyproject.toml
└── README.md
```

## Documentação

- [Arquitetura](docs/architecture.md)
- [Ambiente de desenvolvimento](docs/development.md)
- [Guia de uso](docs/user-guide.md)
- [Modelo da simulação](docs/simulation-model.md)
- [Inventário da implementação](docs/implementation-inventory.md)
- [Roadmap](docs/roadmap.md)
- [Glossário](docs/glossary.md)
- [Decisões arquiteturais](docs/decisions/README.md)
- [Processo de especificações](docs/specs/README.md)
- [Como contribuir](CONTRIBUTING.md)
- [Histórico de mudanças](CHANGELOG.md)

## Processo de desenvolvimento

O projeto adota uma abordagem híbrida de documentação:

- documentação clássica descreve o sistema existente;
- ADRs registram decisões duradouras;
- specs definem novas funcionalidades e mudanças de comportamento antes da
  implementação.

Uma mudança pequena que apenas restaura um comportamento já definido não exige
uma spec própria. Consulte o [guia de especificações](docs/specs/README.md).

## Licença

Distribuído sob a licença MIT. Consulte [LICENSE](LICENSE).
