# Design: transporte reverso

## Estado

Proposta associada à spec ainda em `Draft`. Este documento não autoriza a
implementação antes da resolução das questões em aberto e aprovação da spec.

## Solução proposta

A RPM será tratada como grandeza com sinal. `REW` usará -2600 RPM e a velocidade
angular herdará diretamente esse sinal.

O cálculo do atrito deverá reduzir o módulo da velocidade-alvo, sem forçar seu
sinal para positivo. Uma formulação possível é calcular primeiro o módulo da
carga e aplicá-la na direção oposta ao setpoint.

## Mudanças previstas

- Usar o domínio já extraído em `sim/model.py`, sem dependência de Qt.
- Alterar o setpoint de `REW`.
- Remover o limite inferior de zero da RPM.
- Tornar o cálculo de atrito simétrico em relação ao sinal.
- Preservar o sinal ao aplicar jitter e calcular ângulos.
- Cobrir transições entre parado, avanço e retrocesso.

## Alternativas consideradas

### Direção em variável separada

Manter RPM sempre positiva e armazenar a direção em outro campo. Isso torna
gráficos, erro de controle e transições mais complexos, portanto não é a opção
preferida.

### RPM com sinal

Usar o próprio sinal para representar a direção. É a opção proposta por manter
uma interpretação consistente entre estado, controle, telemetria e animação.

## Riscos

- O uso atual de `abs()` e `max(..., 0)` pode esconder hipóteses de sentido
  único.
- Uma inversão direta pode atravessar zero rápido demais para um modelo físico.
- O ruído pode provocar inversões visuais breves perto de zero.

## Validação proposta

- Testes unitários para os requisitos `RF-01`, `RF-02`, `RF-06` e `RF-07`.
- Teste manual da animação para `RF-03` e `RF-04`.
- Teste automatizado dos dados destinados à telemetria para `RF-05`.

## Preparação já concluída

O núcleo já foi extraído de `app.py` e possui testes de caracterização. Isso
atende à infraestrutura necessária para `RNF-01`, mas não implementa os
requisitos funcionais desta spec.
