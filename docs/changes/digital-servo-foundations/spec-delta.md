# Delta: fundamentos do servo digital

## Specs afetadas

- `docs/specs/speed-control/spec.md`
- `docs/specs/fault-injection/spec.md`
- `docs/specs/telemetry-and-plots/spec.md`
- `docs/specs/simulation-runtime/spec.md`

## Requisitos modificados

### SC-RF-02

**Vigente:** o comando é proporcional ao erro, com `Kp = 0.02`.

**Proposto:** em `Digital Tach ON`, o comando deve ser calculado por um PID
configurável; em `OFF`, a planta deve receber um comando nominal sem correção por
realimentação.

### FI-RF-06

**Vigente:** jitter gaussiano afeta somente a velocidade visual.

**Proposto:** falhas de medição permanecem no encoder; wow e flutter atuam sobre
a velocidade física da planta.

## Requisitos adicionados

- **SC-RF-08:** O controle digital deve poder alternar entre `OFF` e `ON`.
- **SC-RF-09:** Em `ON`, o PID deve usar a medição do encoder.
- **SC-RF-10:** `OFF` deve manter o comando nominal fixo; `ON` deve somar a ele a
  correção PID.
- **SC-RF-11:** O atuador deve usar `[-1, +1]`, `plant_max_rpm = 3000`
  configurável e nominal `setpoint_rpm / plant_max_rpm`.
- **SC-RF-12:** `OFF → ON` deve usar `transfer_bias` com correção inicial zero;
  bias e saída `ON → OFF` devem decair em `250 ms`.
- **SC-RF-13:** A derivada deve atuar sobre a medição.
- **SC-RF-14:** O anti-windup deve usar integração condicional e limitar o termo
  integral à margem disponível do atuador.
- **FI-RF-08:** Wow e flutter devem ser reproduzíveis.
- **FI-RF-09:** Ativação, frequência e amplitude devem mudar em execução dentro
  das faixas do design.
- **FI-RF-10:** Devem existir presets `Wow`, `Flutter`, `Combined` e restauração
  dos padrões.
- **FI-RF-11:** Alterações devem preservar fase e suavizar amplitude.
- **TP-RF-10:** A telemetria deve distinguir nominal, `P/I/D`, `transfer_bias`,
  comandos solicitado/aplicado, saturação e bloqueio integral.
- **SR-RF-07:** Planta, perturbações, encoder e PID devem usar passo de `1 ms`
  independente da GUI.
- **SR-RF-08:** O runtime deve limitar recuperação a `100 ms`, sinalizar e
  excluir o excedente das métricas.

## Critérios de aceitação adicionados

### DSF-CA-01: decomposição preserva o baseline

- **Dado** o comportamento caracterizado do protótipo;
- **Quando** planta, controlador, encoder e falhas são separados;
- **Então** os seis testes vigentes devem continuar passando antes da ativação
  dos novos modelos.

### DSF-CA-02: perturbações configuráveis

- **Dado** o mesmo perfil, parâmetros e instante inicial;
- **Quando** duas execuções são realizadas;
- **Então** a planta deve receber a mesma perturbação;
- **E** ajustes em execução devem preservar fase e suavizar amplitude.

### DSF-CA-03: base nominal

- **Dado** `plant_max_rpm = 3000` e setpoint de `1800 RPM`;
- **Quando** `OFF` está ativo sem carga ou perturbação;
- **Então** o nominal deve ser `0,60` e sustentar o setpoint.

### DSF-CA-04: núcleo desacoplado

- **Dado** intervalo de GUI de `16 ms`;
- **Quando** o runtime avança;
- **Então** deve executar dezesseis passos de `1 ms`;
- **E** limitar e sinalizar atrasos superiores a `100 ms`.

### DSF-CA-05: transferência suave

- **Dado** `OFF` com erro diferente de zero e qualquer valor de `Ki`;
- **Quando** `ON` é ativado;
- **Então** a primeira correção deve ser zero e o bias deve decair em `250 ms`;
- **E** `ON → OFF` deve parar a realimentação e remover a correção em `250 ms`.

### DSF-CA-06: anti-windup

- **Dado** saturação positiva;
- **Quando** erro positivo tenta aprofundá-la;
- **Então** a integral deve ser bloqueada;
- **Mas** erro negativo deve permitir integração para sair da saturação.
