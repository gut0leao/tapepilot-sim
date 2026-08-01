# Controle de velocidade

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir como o protótipo calcula comando e evolução da RPM.

## Escopo

- Erro de velocidade.
- Controle proporcional e saturação.
- Resposta de primeira ordem.
- Convergência em `STOP`.

## Fora de escopo

- PID, encoder discreto e parâmetros identificados em hardware.
- Seleção dos setpoints.
- Efeitos específicos das falhas.

## Requisitos funcionais

- **SC-RF-01:** O erro deve ser `rpm_setpoint - rpm`.
- **SC-RF-02:** O comando deve ser `Kp × erro`, com `Kp = 0.02`.
- **SC-RF-03:** O comando deve ser limitado à faixa de -1 a 1.
- **SC-RF-04:** A RPM deve seguir o alvo por resposta de primeira ordem com
  `tau = 0.25 s` e `alpha = dt / (tau + dt)`.
- **SC-RF-05:** Em `STOP`, uma RPM positiva deve convergir para zero sem ficar
  negativa.

## Requisitos não funcionais

- **SC-RNF-01:** O controle e a dinâmica devem ser testáveis sem Qt.
- **SC-RNF-02:** Os parâmetros vigentes devem permanecer explícitos no modelo.

## Critérios de aceitação

### SC-CA-01: saturação

- **Dado** um erro de grande magnitude;
- **Quando** um passo é executado;
- **Então** o módulo do PWM não deve ultrapassar 1.

### SC-CA-02: resposta nominal

- **Dado** `PLAY`, RPM inicial zero, `dt = 0.25 s` e ausência de atrito;
- **Quando** um passo é executado;
- **Então** a RPM deve ser 900.

### SC-CA-03: parada

- **Dado** RPM positiva;
- **Quando** passos sucessivos em `STOP` são executados;
- **Então** a RPM deve diminuir em direção a zero.

## Limitações vigentes

- O controlador não possui termos integral ou derivativo.
- Não há saturação física de torque nem discretização do atuador.
- O modelo não valida `dt` inválido.

## Evidências

- **Código:** `sim/model.py`.
- **Testes:** `test_pwm_is_saturated`,
  `test_first_order_response_uses_elapsed_time` e
  `test_stop_converges_toward_zero`.
- **Validação manual:** resposta observada nos gráficos em 2026-07-31.

