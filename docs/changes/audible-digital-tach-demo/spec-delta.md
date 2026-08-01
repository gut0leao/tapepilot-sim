# Delta: demonstração audível do servo digital

## Specs afetadas

- `docs/specs/transport-modes/spec.md`
- `docs/specs/speed-control/spec.md`
- `docs/specs/fault-injection/spec.md`
- `docs/specs/telemetry-and-plots/spec.md`
- `docs/specs/simulation-runtime/spec.md`
- nova spec `docs/specs/audio-playback/spec.md` após implementação

## Requisitos modificados

### SC-RF-02

**Vigente:** o comando é proporcional ao erro, com `Kp = 0.02`.

**Proposto:** em `Digital Tach ON`, o comando deve ser calculado por um PID
configurável; em `OFF`, a planta deve receber um comando nominal sem correção por
realimentação.

### FI-RF-06

**Vigente:** jitter gaussiano afeta somente a velocidade visual.

**Proposto:** falhas de medição permanecem no encoder; perturbações de wow e
flutter devem atuar sobre a velocidade física da planta.

## Requisitos adicionados

- **SC-RF-08:** O controle digital deve poder ser alternado entre `OFF` e `ON`
  durante a simulação.
- **SC-RF-09:** Em `ON`, o controlador deve usar a medição do encoder para
  reduzir o erro da velocidade física.
- **SC-RF-10:** O comando nominal deve atingir o setpoint em regime permanente
  na planta nominal sem perturbação ou carga adicional; `OFF` deve mantê-lo fixo
  e `ON` deve somar a ele a correção do PID.
- **SC-RF-11:** O atuador deve aceitar comando normalizado em `[-1, +1]`; a
  planta deve usar `plant_max_rpm = 3000` configurável, calcular o nominal por
  `setpoint_rpm / plant_max_rpm` e saturar a soma do nominal com a correção PID.
- **SC-RF-12:** A troca `OFF → ON` deve inicializar a derivada pela medição atual
  e usar `transfer_bias` para que a correção comece em zero, inclusive com
  `Ki = 0`; o bias deve decair a zero em `250 ms`. Em `ON → OFF`, o PID deve
  parar de atualizar, reduzir sua última correção linearmente a zero em `250 ms`
  e limpar seus estados ao final.
- **SC-RF-13:** O termo derivativo deve ser calculado sobre a medição para evitar
  pico causado por mudanças de setpoint.
- **SC-RF-14:** O PID deve bloquear a integração quando o erro aprofundar a
  saturação, permiti-la quando ajudar a sair da saturação e limitar o termo
  integral à margem entre o comando nominal e os limites `[-1, +1]`.
- **FI-RF-08:** Perfis de wow e flutter devem ser reproduzíveis com os mesmos
  parâmetros e semente.
- **FI-RF-09:** Ativação, frequência e amplitude de wow e flutter devem ser
  configuráveis durante a simulação dentro das faixas definidas no design.
- **FI-RF-10:** Devem existir os presets demonstrativos `Wow`, `Flutter` e
  `Combined`, além de uma ação para restaurar seus valores padrão.
- **FI-RF-11:** Alterações em tempo de execução devem preservar a continuidade
  de fase e aplicar transição suave de amplitude.
- **TP-RF-08:** A interface deve mostrar o estado `Digital Tach OFF/ON`.
- **TP-RF-09:** A comparação deve apresentar erro RMS, desvio máximo, overshoot
  e tempo em saturação.
- **TP-RF-10:** A telemetria deve distinguir comando nominal, termos `P/I/D`,
  `transfer_bias`, comandos solicitado e aplicado, saturação e bloqueio da
  integral.
- **SR-RF-06:** O processamento de áudio não deve bloquear o loop da interface.
- **SR-RF-07:** Planta, perturbações, encoder e PID devem avançar com passo fixo
  de `1 ms`, independentemente do intervalo de atualização da GUI.
- **SR-RF-08:** O runtime deve acumular tempo monotônico, limitar a recuperação a
  `100 ms` por atualização, sinalizar o descarte do excedente e excluí-lo das
  métricas comparativas.

## Nova capacidade proposta: audio-playback

- **AP-RF-01:** Uma amostra WAV PCM deve poder ser carregada para demonstração.
- **AP-RF-02:** O áudio deve tocar somente no modo `PLAY` no MVP.
- **AP-RF-03:** A taxa instantânea deve derivar de
  `tape_speed / nominal_tape_speed`.
- **AP-RF-04:** O áudio deve usar a velocidade física da planta, não diretamente
  a medição do encoder ou o comando do controlador.
- **AP-RF-05:** A mesma amostra deve permitir perceber a transição entre
  `Digital Tach OFF` e `ON`.
- **AP-RNF-01:** A reprodução não deve introduzir interrupções que confundam a
  avaliação do controlador.

## Critérios de aceitação adicionados

### ADT-CA-01: perturbação reproduzível

- **Dado** o mesmo perfil, parâmetros e semente;
- **Quando** duas execuções são realizadas;
- **Então** a planta deve receber a mesma perturbação física.

### ADT-CA-02: comparação OFF/ON

- **Dado** o mesmo perfil de perturbação e uma amostra sustentada;
- **Quando** o controle muda de `OFF` para `ON`;
- **Então** erro de velocidade, wow/flutter audível e métricas devem melhorar
  após o tempo de acomodação.

### ADT-CA-03: origem da modulação

- **Dado** ruído apenas na medição do encoder;
- **Quando** o áudio é gerado;
- **Então** sua taxa deve seguir a velocidade física resultante, e não o ruído
  de medição isoladamente.

### ADT-CA-04: parametrização em tempo de execução

- **Dado** um perfil ativo durante `PLAY`;
- **Quando** frequência ou amplitude é alterada;
- **Então** a nova configuração deve atuar imediatamente sobre a planta sem
  reiniciar a fase ou introduzir um salto descontínuo.

### ADT-CA-05: padrões restauráveis

- **Dado** que os parâmetros foram alterados;
- **Quando** `Restaurar padrão` é acionado;
- **Então** wow deve retornar a `0,5 Hz` e `±1%`, e flutter a `8 Hz` e `±0,3%`.

### ADT-CA-06: base comum da comparação

- **Dado** a planta nominal em regime permanente, sem perturbação ou carga
  adicional;
- **Quando** `Digital Tach OFF` está ativo;
- **Então** o comando nominal fixo deve sustentar o setpoint;
- **E** ao ativar `ON`, a correção do PID deve ser somada à mesma base nominal.

### ADT-CA-07: escala e saturação do atuador

- **Dado** `plant_max_rpm = 3000` e setpoint de `1800 RPM`;
- **Quando** o comando nominal é calculado;
- **Então** ele deve ser `0,60`;
- **E** qualquer comando total deve ser limitado ao intervalo `[-1, +1]`,
  preservando separadamente os valores solicitado e aplicado para telemetria.

### ADT-CA-08: núcleo desacoplado da interface

- **Dado** um intervalo de GUI de `16 ms`;
- **Quando** o runtime atualiza o núcleo;
- **Então** devem ser executados dezesseis passos de `1 ms` antes da apresentação
  do estado;
- **E** um atraso superior a `100 ms` deve ser limitado e sinalizado sem
  contaminar as métricas da demonstração.

### ADT-CA-09: transferência OFF/ON sem salto

- **Dado** `Digital Tach OFF` com erro de velocidade diferente de zero;
- **Quando** `ON` é ativado;
- **Então** o `transfer_bias` deve tornar a primeira correção zero e o comando
  aplicado deve permanecer no valor nominal, inclusive com `Ki = 0`;
- **E** a derivada não deve produzir pico pela troca ou por mudança de setpoint.

### ADT-CA-10: saída suave do controle

- **Dado** `Digital Tach ON` com correção PID diferente de zero;
- **Quando** `OFF` é ativado;
- **Então** o PID deve parar de reagir ao encoder e a correção deve chegar
  linearmente a zero em `250 ms`;
- **E** seus estados internos devem estar limpos ao final da rampa.

### ADT-CA-11: anti-windup condicional

- **Dado** o comando aplicado saturado no limite positivo;
- **Quando** o erro positivo tenta aprofundar a saturação;
- **Então** o termo integral deve permanecer inalterado;
- **Mas**, quando o erro se torna negativo, a integração deve ser permitida para
  ajudar o comando a sair da saturação;
- **E** o termo integral nunca deve exceder a margem disponível em relação ao
  comando nominal.
