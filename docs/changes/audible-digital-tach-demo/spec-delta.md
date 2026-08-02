# Delta: demonstração audível do servo digital

## Dependência

Esta change pressupõe os requisitos da
[change de fundamentos](../archive/2026-08-01-digital-servo-foundations/spec-delta.md).

## Specs afetadas

- `docs/specs/telemetry-and-plots/spec.md`
- `docs/specs/simulation-runtime/spec.md`
- nova spec `docs/specs/audio-playback/spec.md` após implementação

## Requisitos adicionados

- **TP-RF-10:** A interface deve mostrar `Digital Tach OFF/ON` na comparação
  audível.
- **TP-RF-11:** A comparação deve apresentar erro RMS, desvio máximo, overshoot
  e tempo em saturação.
- **SR-RF-09:** O processamento de áudio não deve bloquear a interface.

## Nova capacidade proposta: audio-playback

- **AP-RF-01:** Uma amostra WAV PCM deve poder ser carregada.
- **AP-RF-02:** O áudio deve tocar somente em `PLAY` no MVP.
- **AP-RF-03:** A taxa deve derivar de `tape_speed / nominal_tape_speed`.
- **AP-RF-04:** O áudio deve usar a velocidade física, não encoder ou PID.
- **AP-RF-05:** A mesma amostra deve evidenciar a transição `OFF/ON`.
- **AP-RNF-01:** A reprodução não deve introduzir interrupções que confundam a
  avaliação do controlador.

## Critérios de aceitação adicionados

### ADT-CA-01: origem da modulação

- **Dado** ruído apenas no encoder;
- **Quando** o áudio é gerado;
- **Então** sua taxa deve seguir a velocidade física resultante.

### ADT-CA-02: comparação OFF/ON

- **Dado** a mesma perturbação e uma amostra sustentada;
- **Quando** o controle muda de `OFF` para `ON`;
- **Então** erro de velocidade, efeito audível e métricas devem melhorar após o
  tempo de acomodação.
