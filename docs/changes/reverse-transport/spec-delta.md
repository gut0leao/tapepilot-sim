# Delta: transporte reverso

## Specs afetadas

- `docs/specs/transport-modes/spec.md`
- `docs/specs/speed-control/spec.md`
- `docs/specs/mechanics-visualization/spec.md`
- `docs/specs/telemetry-and-plots/spec.md`

## Requisitos modificados

### TM-RF-06

**Vigente:** `REW` deve usar setpoint de 2600 RPM.

**Proposto:** `REW` deve usar setpoint de -2600 RPM.

### SC-RF-05

**Vigente:** em `STOP`, uma RPM positiva deve convergir para zero sem ficar
negativa.

**Proposto:** em `STOP`, a RPM deve convergir para zero a partir de qualquer
sentido sem ultrapassar zero.

### MV-RF-06

**Vigente:** os componentes usam a velocidade angular visual positiva e seus
fatores atuais.

**Proposto:** o capstan deve preservar o sinal da velocidade angular e girar em
sentido oposto durante `REW`. O comportamento de cada bobina será definido antes
da aprovação desta mudança.

## Requisitos adicionados

- **SC-RF-06:** A RPM simulada deve admitir valores negativos.
- **SC-RF-07:** O atrito deve reduzir o módulo da velocidade-alvo nos dois
  sentidos.
- **TP-RF-06:** Telemetria e gráfico devem exibir RPM e setpoint negativos em
  `REW`.

## Critérios de aceitação adicionados

### RT-CA-01: entrada em REW

- **Dado** o simulador parado;
- **Quando** `REW` é selecionado;
- **Então** o setpoint deve ser -2600 RPM e a RPM deve convergir para um valor
  negativo.

### RT-CA-02: parada após REW

- **Dado** RPM negativa;
- **Quando** `STOP` é selecionado;
- **Então** a RPM deve convergir para zero sem saltar para valor positivo.

### RT-CA-03: atrito e animação

- **Dado** `REW` ativo;
- **Quando** o atrito aumenta;
- **Então** o módulo da RPM deve diminuir e o capstan deve preservar o sentido
  reverso;
- **E** as bobinas devem seguir a decisão registrada antes da aprovação.

## Nota de consistência

Embora adicione `TP-RF-06`, esta proposta não altera a arquitetura de telemetria:
ela já exibe os valores fornecidos pelo estado. A spec `telemetry-and-plots`
deverá receber o requisito ao incorporar o delta.
