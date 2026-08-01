# Transporte reverso

- **Estado:** Draft
- **Responsável:** não definido
- **Data:** 2026-07-31

## Contexto

Atualmente, `FF` e `REW` usam o mesmo setpoint positivo de 2600 RPM. A simulação
não distingue o sentido do avanço rápido e do retrocesso.

## Objetivo

Representar `REW` por meio de velocidade negativa, inclusive na dinâmica,
telemetria, gráficos e animação.

## Fora de escopo

- Motores independentes para cada bobina.
- Modelo físico de frenagem ou inversão.
- Cálculo realista de tensão durante a transição.
- Alteração do comportamento de `PLAY` ou `FF`.

## Requisitos funcionais

- **RF-01:** `REW` deve usar setpoint de -2600 RPM.
- **RF-02:** A RPM simulada deve admitir valores negativos.
- **RF-03:** O capstan deve girar no sentido inverso durante `REW`.
- **RF-04:** As bobinas devem girar no sentido inverso durante `REW`.
- **RF-05:** Telemetria e gráfico devem exibir RPM negativa durante `REW`.
- **RF-06:** `STOP` deve levar a RPM a zero a partir de qualquer sentido.
- **RF-07:** O atrito deve se opor ao movimento nos dois sentidos.

## Requisitos não funcionais

- **RNF-01:** A dinâmica do transporte deve ser testável sem abrir a interface.
- **RNF-02:** O comportamento existente de `PLAY`, `FF`, `PAUSE` e `STOP` deve
  permanecer compatível, exceto onde esta spec disser o contrário.

## Critérios de aceitação

### Cenário 1: entrada em REW

- **Dado** que o simulador está parado;
- **Quando** o usuário seleciona `REW`;
- **Então** o setpoint passa a -2600 RPM;
- **E** a RPM converge para um valor negativo.

### Cenário 2: parada após REW

- **Dado** que a RPM é negativa;
- **Quando** o usuário seleciona `STOP`;
- **Então** a RPM converge continuamente para zero;
- **E** não salta para um valor positivo.

### Cenário 3: animação reversa

- **Dado** que o transporte está em `REW`;
- **Quando** a simulação avança;
- **Então** os ângulos das bobinas e do capstan variam no sentido oposto ao de
  `FF`.

### Cenário 4: atrito em REW

- **Dado** que o transporte está em `REW`;
- **Quando** o atrito aumenta;
- **Então** o módulo da RPM em regime diminui.

## Casos extremos

- Transição direta entre `FF` e `REW`.
- `dt` nulo ou excepcionalmente grande.
- Jitter próximo da passagem por zero.
- Atrito máximo nos dois sentidos.

## Questões em aberto

- A reversão deve ser imediata ou exigir uma fase de frenagem?
- As duas bobinas devem sempre compartilhar o mesmo sinal de rotação visual?

## Evidências de implementação

- **Preparação existente:** o núcleo está em `sim/model.py` e pode ser testado
  sem Qt, atendendo antecipadamente ao `RNF-01`.
- **Testes existentes:** `tests/test_simulator.py` caracteriza o comportamento
  atual, inclusive `REW` ainda positivo.
- **Requisitos funcionais:** nenhum implementado; a spec permanece em `Draft`.
