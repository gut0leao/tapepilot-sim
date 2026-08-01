# Guia de uso

## Iniciando

Execute `python3 app.py` na raiz do repositório. A aplicação abre uma janela de
1200 × 700 px intitulada “TapePilot V1 - Simulador (WSL/Qt/SVG)”.

A tela é dividida em:

- cena mecânica com duas bobinas e um capstan;
- painel de transporte, falhas e telemetria;
- quatro gráficos na parte inferior.

## Controles de transporte

| Controle | Comportamento atual |
|---|---|
| `STOP` | define setpoint de 0 RPM |
| `PLAY` | define setpoint de 1800 RPM |
| `PAUSE` | define setpoint de 300 RPM |
| `FF` | define setpoint de 2600 RPM |
| `REW` | define setpoint de 2600 RPM |

`REW` ainda não inverte o sentido. Esse comportamento está registrado como
limitação e possui uma proposta de mudança em elaboração.

## Injeção de falhas

Os dois sliders possuem valores inteiros de 0 a 100, convertidos internamente
para a faixa de 0 a 1.

### Atrito da fita

Reduz a velocidade-alvo e aumenta o indicador de tensão. O efeito é uma
heurística visual, sem unidade física.

### Jitter do encoder

Adiciona ruído gaussiano à velocidade usada para animar as peças. Apesar do
nome, ele ainda não altera a RPM realimentada, a telemetria ou o gráfico.

## Telemetria

O painel mostra:

- modo de transporte;
- RPM simulada e setpoint;
- PWM e erro;
- níveis de atrito e jitter;
- tensão simulada.

O texto pode ser selecionado com o mouse.

## Gráficos

Os gráficos são atualizados em tempo real e preservam os últimos 20 segundos:

- RPM desejada e simulada;
- PWM/comando;
- erro de controle;
- tensão simulada.

As duas curvas do gráfico de RPM ainda não possuem legenda própria. Os gráficos
usam antialiasing para melhorar a apresentação.

## Cena mecânica

As bobinas possuem largura visual de 180 px e o capstan, 70 px. As peças giram
em torno do centro de seus respectivos SVGs. Os fatores de velocidade são
apenas visuais e não representam relações mecânicas reais.

## Limitações de operação

- Não há configuração de parâmetros pela interface além dos dois sliders.
- Não há persistência ou exportação de dados.
- Não há pausa do relógio da simulação; `PAUSE` é um modo de baixa velocidade.
- Não há indicação visual do botão atualmente selecionado.
- Os caminhos dos SVGs dependem da execução na raiz do projeto.
