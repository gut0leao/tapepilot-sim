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
- **FI-RF-09:** Ocorrência, duração média, taxa característica e intensidade
  `Dry/Wet` devem mudar em execução dentro das faixas do design.
- **FI-RF-10:** Wow e flutter devem possuir controles independentes; seus sinais
  devem ser somados quando ambos estiverem ativos, sem estado `Combined`.
- **FI-RF-12:** `Restaurar padrão` deve zerar a ocorrência de ambos e recuperar
  `0,5 Hz/1%/3 s` para wow e `8 Hz/0,3%/0,5 s` para flutter.
- **FI-RF-13:** Wow e flutter devem usar ruído filtrado dominante, envelope de
  presença variável, periodicidade residual e sementes fixas independentes.
- **FI-RF-14:** Wow e flutter devem ocorrer em episódios independentes. A
  ocorrência deve representar a proporção média do tempo ativo; episódios e
  intervalos devem variar entre `50%` e `150%` de suas durações médias.
- **FI-RF-15:** O encoder deve gerar `100 pulsos/revolução`, acumular pulsos em
  passos de `1 ms` e atualizar a RPM medida em janelas de `10 ms`.
- **FI-RF-16:** Jitter do encoder deve adicionar ruído gaussiano reproduzível,
  escalado até `20 RPM`, com semente fixa `3301`.
- **FI-RF-17:** Perda de pulsos deve ser ajustável de `0%` a `100%`; dropout
  ativo deve descartar todos os pulsos gerados.
- **FI-RF-18:** A medição bruta deve alimentar um filtro passa-baixas de
  primeira ordem com constante de tempo inicial de `50 ms`.
- **SC-RF-15:** O futuro PID deve usar a RPM filtrada; dropout deve permanecer
  explícito e não ser inferido da saída do filtro.
- **TP-RF-11:** Contagem acumulada de pulsos, RPM medida, perda configurada e
  estado de dropout devem estar disponíveis no estado e na telemetria.
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

### DSF-CA-07: controles independentes

- **Dado** ocorrência zero para wow e positiva para flutter;
- **Quando** a simulação avança;
- **Então** apenas flutter deve contribuir para a perturbação;
- **E**, quando ambos estiverem ligados, a saída deve ser a soma dos dois sem
  registrar um terceiro estado.

### DSF-CA-08: irregularidade reproduzível

- **Dado** os mesmos parâmetros, sementes e instante inicial;
- **Quando** duas execuções usam os mesmos controles;
- **Então** devem produzir amostras idênticas;
- **E** wow e flutter devem usar sequências diferentes;
- **E** o sinal não deve repetir a antiga senoide após um período característico.

### DSF-CA-09: episódios naturais

- **Dado** ocorrência zero;
- **Quando** a simulação avança;
- **Então** a perturbação deve permanecer ausente;
- **E**, com ocorrência intermediária, devem existir episódios ativos e
  inativos reproduzíveis;
- **E**, com ocorrência máxima, a perturbação deve permanecer ativa.

### DSF-CA-10: encoder discreto e falhas

- **Dado** `600 RPM`, `100 pulsos/revolução` e uma janela de `10 ms`;
- **Quando** não há perda, jitter ou dropout;
- **Então** o encoder deve observar `10` pulsos e estimar `600 RPM`;
- **E**, com perda máxima ou dropout, deve observar zero pulsos e zero RPM;
- **E** execuções com os mesmos parâmetros devem produzir medições idênticas.

### DSF-CA-11: encoder ainda não fecha a malha

- **Dado** dropout ativo durante `PLAY`;
- **Quando** a simulação avança antes da Issue #7;
- **Então** a medição do encoder deve ser zero;
- **Mas** planta, controlador e animação devem continuar usando a RPM física.

### DSF-CA-12: filtragem da medição

- **Dado** um sinal físico constante sem falhas;
- **Quando** o encoder produz degraus de quantização;
- **Então** a RPM bruta deve permanecer observável;
- **E** a RPM filtrada deve convergir para a medição bruta estável.

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
