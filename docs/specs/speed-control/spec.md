# Controle de velocidade

- **Estado:** Implemented
- **Última atualização:** 2026-08-01

## Propósito

Definir comando nominal, controle digital e evolução da RPM física.

## Escopo

- Digital Tach OFF/ON/FALLBACK.
- Controlador PI/PID ajustável, saturação e anti-windup.
- Transições suaves e resposta de primeira ordem.

## Fora de escopo

- Parâmetros calibrados em hardware e sentido reverso.
- Seleção dos setpoints e processamento de áudio.

## Requisitos funcionais

- **SC-RF-01:** O erro deve ser `rpm_setpoint - encoder_rpm_filtered`.
- **SC-RF-02:** Em `OFF`, o comando deve ser nominal; em `ON`, deve somar a
  correção PI/PID calculada com a medição filtrada do encoder.
- **SC-RF-03:** O comando aplicado deve ser limitado a `[-1,+1]`.
- **SC-RF-04:** A RPM deve seguir o alvo por resposta de primeira ordem com
  `tau = 0.25 s` e `alpha = dt / (tau + dt)`.
- **SC-RF-05:** Em `STOP`, uma RPM positiva deve convergir para zero.
- **SC-RF-08:** O controle digital deve alternar entre `OFF` e `ON` em execução.
- **SC-RF-09:** Em `ON`, o PID deve usar a RPM filtrada do encoder.
- **SC-RF-10:** A correção PI/PID deve ser somada ao comando nominal.
- **SC-RF-11:** O atuador deve usar `[-1,+1]`, `plant_max_rpm = 3000` e
  nominal `setpoint_rpm / plant_max_rpm`.
- **SC-RF-12:** Transições OFF/ON devem retirar bias ou correção em `250 ms`,
  começando sem salto.
- **SC-RF-13:** A derivada deve atuar sobre a medição.
- **SC-RF-14:** A integral deve ser condicional durante saturação e limitada à
  margem disponível do atuador.
- **SC-RF-15:** O PID deve usar a RPM filtrada; dropout permanece explícito.
- **SC-RF-16:** Dropout em `ON` deve ativar `FALLBACK`, retirar a correção em
  `250 ms` e retomá-la suavemente quando o sinal voltar.
- **SC-RF-17:** A derivada deve usar o intervalo real entre novas medições do
  encoder e manter seu valor até a próxima amostra.

## Requisitos não funcionais

- **SC-RNF-01:** Controle e dinâmica devem ser testáveis sem Qt.
- **SC-RNF-02:** Parâmetros devem permanecer explícitos no modelo.
- **SC-RNF-03:** No benchmark vigente, RMS de até `0,1%` é a meta e até `0,2%`
  é o limite aceitável provisório.

## Critérios de aceitação

### SC-CA-01: comando nominal

- **Dado** `PLAY`, `plant_max_rpm = 3000` e Digital Tach OFF;
- **Quando** o comando é calculado;
- **Então** deve ser `0,60` e sustentar `1800 RPM` na planta nominal.

### SC-CA-02: transferência suave

- **Dado** erro diferente de zero;
- **Quando** Digital Tach alterna entre OFF e ON;
- **Então** o primeiro comando não deve saltar e a transição deve durar `250 ms`.

### SC-CA-03: anti-windup

- **Dado** saturação positiva;
- **Quando** erro positivo tenta aprofundá-la;
- **Então** a integral deve ser bloqueada e liberada para erro contrário.

### SC-CA-04: fallback

- **Dado** Digital Tach ON;
- **Quando** ocorre dropout;
- **Então** o comando deve convergir ao nominal e retomar o PID sem salto.

### SC-CA-05: benchmark

- **Dado** o perfil padrão documentado no modelo;
- **Quando** os `3 s` iniciais são descartados e `5 s` são medidos;
- **Então** o RMS físico deve ser classificado pela meta de `0,1%` e limite de
  `0,2%`.

## Limitações vigentes

- Ganhos e planta não foram calibrados em hardware.
- `Kd` inicia em zero devido à quantização residual do encoder.
- Não há saturação física de torque nem validação de `dt` inválido.

## Evidências

- **Código:** `sim/controller.py`, `sim/model.py`, `sim/plant.py`.
- **Testes:** testes de PID em `test_components.py`, `test_simulator.py` e
  cenários `wow_tach_on`, `wow_max_tach_on` e `dropout_fallback`.
- **Validação manual:** controle, transições e perturbações aprovados em 2026-08-01.

