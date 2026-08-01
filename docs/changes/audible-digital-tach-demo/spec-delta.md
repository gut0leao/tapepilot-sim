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
- **FI-RF-08:** Perfis de wow e flutter devem ser reproduzíveis com os mesmos
  parâmetros e semente.
- **TP-RF-08:** A interface deve mostrar o estado `Digital Tach OFF/ON`.
- **TP-RF-09:** A comparação deve apresentar erro RMS, desvio máximo, overshoot
  e tempo em saturação.
- **SR-RF-06:** O processamento de áudio não deve bloquear o loop da interface.

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
