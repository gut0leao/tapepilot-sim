# Injeção de falhas

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir as perturbações ajustáveis e seus efeitos vigentes.

## Escopo

- Atrito da fita.
- Jitter usado na animação.
- Indicador simulado de tensão.

## Fora de escopo

- Dropout, perda de pulsos, escorregamento e back-tension.
- Modelo físico calibrado de tensão.

## Requisitos funcionais

- **FI-RF-01:** A interface deve oferecer sliders de atrito e jitter de 0 a 100.
- **FI-RF-02:** Os sliders devem ser convertidos para valores de 0 a 1.
- **FI-RF-03:** A carga de atrito deve ser `tape_friction × 600`.
- **FI-RF-04:** O atrito deve reduzir o alvo por
  `friction_load × abs(pwm)`.
- **FI-RF-05:** A tensão deve ser
  `tape_friction × (0.3 + 0.7 × abs(pwm))`.
- **FI-RF-06:** O jitter deve ser gaussiano, escalado por
  `encoder_jitter × 20`, e afetar somente a velocidade visual.
- **FI-RF-07:** A velocidade visual não deve ficar abaixo de zero.

## Requisitos não funcionais

- **FI-RNF-01:** A telemetria deve indicar os níveis das falhas e a tensão.

## Critérios de aceitação

### FI-CA-01: atrito

- **Dado** o mesmo modo e estado inicial;
- **Quando** uma simulação usa atrito máximo e outra não usa atrito;
- **Então** a primeira deve produzir RPM menor e tensão positiva.

### FI-CA-02: controles

- **Dado** que a janela está aberta;
- **Quando** os sliders são movidos aos extremos;
- **Então** o estado deve receber respectivamente 0 e 1.

## Limitações vigentes

- O jitter não afeta controle, telemetria de RPM ou gráficos.
- A tensão não possui unidade e não realimenta a planta.
- Não há validação de faixa para alterações feitas diretamente no estado.

## Evidências

- **Código:** `sim/model.py`, `app.py`.
- **Testes:** `test_friction_reduces_speed_and_produces_tension` cobre
  `FI-RF-03` a `FI-RF-05` qualitativamente.
- **Validação manual:** sliders e telemetria validados em 2026-07-31.

