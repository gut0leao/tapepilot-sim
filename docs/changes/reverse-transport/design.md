# Design: transporte reverso

## Solução proposta

A RPM será uma grandeza com sinal. O setpoint de `REW` passará a -2600 RPM e a
velocidade angular herdará esse sinal.

O atrito deverá reduzir o módulo do alvo sem forçar seu sinal para positivo. A
formulação final depende da decisão sobre a transição entre sentidos.

## Preparação concluída

O núcleo já está em `sim/model.py`, sem dependência de Qt, e possui testes que
caracterizam o comportamento positivo vigente.

## Alternativas

### Direção separada da RPM

Manter RPM positiva e direção em outro campo. Não é preferida porque complica
erro, gráficos e transições.

### RPM com sinal

Usar o sinal da RPM como direção. É a alternativa preferida por manter estado,
controle, telemetria e animação coerentes.

## Riscos

- `abs()` e `max(..., 0)` atuais assumem sentido único.
- Uma inversão direta pode ser rápida demais para um modelo físico.
- Jitter próximo de zero pode gerar inversões visuais breves.

