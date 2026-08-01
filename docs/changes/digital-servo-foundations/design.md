# Design: fundamentos do servo digital

## Componentes

```mermaid
flowchart LR
    Setpoint --> Feedforward[Comando nominal]
    Feedforward --> Sum[Soma]
    PID --> Sum
    Sum --> Saturation[Saturação do atuador]
    Saturation --> Plant[Planta]
    Disturbance[Wow / flutter] --> Plant
    Plant --> Speed[Velocidade física]
    Speed --> Encoder
    Encoder --> PID
    Speed --> Metrics[Métricas]
```

`sim/model.py` permanece como fachada compatível enquanto responsabilidades são
extraídas para módulos próprios. Essa etapa deve preservar o comportamento
vigente antes de ativar os novos modelos.

## Escala e comando nominal

O atuador usa comando adimensional em `[-1, +1]` e a planta usa
`plant_max_rpm = 3000` configurável:

```text
comando_nominal = setpoint_rpm / plant_max_rpm
comando_solicitado = comando_nominal + correção_PID
comando_aplicado = clamp(comando_solicitado, -1, +1)
rpm_alvo = comando_aplicado * plant_max_rpm
```

Tempo usa segundos; velocidade, setpoint e erro usam RPM; perturbações usam
hertz e fração; ângulos visuais usam graus.

## Temporização

```mermaid
flowchart LR
    Clock[Tempo monotônico] --> Accumulator[Acumulador]
    Accumulator --> FixedSteps[Passos fixos de 1 ms]
    FixedSteps --> State[Estado mais recente]
    State --> GUI[GUI a aproximadamente 60 Hz]
```

Planta, perturbações, encoder e PID compartilham inicialmente `1000 Hz`. A
recuperação por tick é limitada a `100 ms`; o excedente é sinalizado e excluído
das métricas.

## Perturbações

| Componente | Padrão | Taxa característica | Intensidade Dry/Wet |
|---|---:|---:|---:|
| Wow | `0,5 Hz`, `±1%` | `0,1–2,0 Hz` | `0–3%` |
| Flutter | `8 Hz`, `±0,3%` | `2–20 Hz` | `0–1%` |

Wow e flutter possuem ativação, frequência e amplitude independentes. Quando
ambos estão ativos, seus sinais são apenas somados; `Combined` não é estado nem
preset. `Restaurar padrão` desliga ambos e recupera os valores da tabela.
Parâmetros mudam em execução preservando a fase residual, e intensidade usa
rampa de `100 ms`.
A perturbação modula a efetividade do acionamento antes da dinâmica da planta.

Cada componente mistura ruído filtrado, envelope lento e uma senoide residual:

| Componente | Ruído | Senoide | Semente | Envelope |
|---|---:|---:|---:|---:|
| Wow | `85%` | `15%` | `1103` | `2 s` |
| Flutter | `90%` | `10%` | `2207` | `500 ms` |

O ruído escolhe novos alvos a cada meio período característico e os suaviza por
`período / 2π`. O envelope usa outra sequência, com semente consecutiva, e varia
a presença entre aproximadamente `30%` e `100%`. A taxa em hertz controla a
velocidade média das irregularidades, não uma senoide exata.

## PID e transições

Em `OFF`, a planta recebe somente o comando nominal fixo. Em `ON`, recebe a
mesma base somada ao PID. A derivada atua sobre a medição.

Em `OFF → ON`, `transfer_bias = -(P + I + D)` produz correção inicial zero e
decai em `250 ms`, inclusive com `Ki = 0`. Em `ON → OFF`, o PID deixa de reagir
ao encoder e sua última correção decai em `250 ms`; os estados são então limpos.

## Anti-windup e telemetria

A integral é bloqueada quando o erro aprofunda a saturação e liberada quando
ajuda a sair dela. Seu termo fica entre `-1 - comando_nominal` e
`+1 - comando_nominal`. Back-calculation fica fora do MVP.

A telemetria distingue comando nominal, `P`, `I`, `D`, `transfer_bias`, comandos
solicitado e aplicado, saturação, tempo saturado e bloqueio da integral.

## Riscos

- A decomposição pode alterar acidentalmente o baseline.
- Parâmetros demonstrativos podem ser confundidos com dados físicos.
- Um PID ajustado apenas na simulação pode não transferir para hardware.
