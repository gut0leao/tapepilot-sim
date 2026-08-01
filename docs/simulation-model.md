# Modelo da simulação

## Propósito e validade

O modelo atual existe para demonstrar o loop de controle e sua visualização. Ele
é qualitativo: os valores não foram identificados a partir de um mecanismo real
e não devem ser usados como previsões físicas.

`Simulator`, em `sim/model.py`, coordena componentes separados para estado,
controle proporcional, planta de primeira ordem, falhas e medição visual. Essa
separação preserva as equações descritas abaixo; os novos modelos aprovados ainda
não estão ativos.

## Estado

As variáveis principais são:

| Variável | Significado | Unidade/faixa |
|---|---|---|
| `rpm_setpoint` | velocidade desejada | RPM |
| `rpm` | velocidade simulada | RPM |
| `pwm` | comando normalizado | -1 a 1 |
| `err` | erro de velocidade | RPM |
| `tape_friction` | intensidade do atrito | 0 a 1 |
| `encoder_jitter` | intensidade do ruído | 0 a 1 |
| `tension` | indicador visual de tensão | sem unidade |

## Modos de transporte

| Modo | Setpoint atual |
|---|---:|
| `STOP` | 0 RPM |
| `PLAY` | 1800 RPM |
| `PAUSE` | 300 RPM |
| `FF` | 2600 RPM |
| `REW` | 2600 RPM |

`REW` ainda não representa uma velocidade negativa. A mudança está proposta em
`docs/changes/reverse-transport/`.

Qualquer string diferente de `PLAY`, `FF`, `REW` e `PAUSE` recebe setpoint zero,
embora seu texto seja preservado no campo `transport`. Não há validação explícita
dos nomes de modo.

## Controlador proporcional

O erro e o comando são calculados por:

```text
error = rpm_setpoint - rpm
pwm = clamp(Kp × error, -1, 1)
Kp = 0.02
```

Não existem termos integral ou derivativo.

## Dinâmica do motor

A RPM segue um alvo por uma aproximação de primeira ordem:

```text
alpha = dt / (tau + dt)
rpm[n+1] = (1 - alpha) × rpm[n] + alpha × target
tau = 0.25 s
```

O `dt` é o tempo real transcorrido entre atualizações da interface.

## Atrito

O slider produz uma carga equivalente em RPM:

```text
friction_load = tape_friction × 600
target = rpm_setpoint - friction_load × abs(pwm)
target = max(target, 0)
```

Essa fórmula é uma heurística e não uma equação mecânica. O limite inferior em
zero também impede, no estado atual, a representação do sentido reverso.

## Jitter

O ruído é gaussiano:

```text
jitter = normal(μ=0, σ=1) × encoder_jitter × 20
rpm_visual = max(rpm + jitter, 0)
```

`rpm_visual` é usado somente para calcular os ângulos. O controlador e o gráfico
de RPM continuam usando `rpm` sem ruído. Portanto, o nome “jitter do encoder” é
uma aproximação da intenção futura, não um encoder modelado.

## Wow e flutter em revisão

A implementação em revisão combina ruído filtrado, envelope variável e uma
pequena senoide residual para modular o alvo físico da planta. Wow usa padrão
`0,5 Hz` e `1%`; flutter, `8 Hz` e `0,3%`.
Cada componente pode ser ligado e ajustado independentemente na interface. Se
ambos estiverem ativos, seus sinais são somados sem criar um estado adicional.
Uma rampa de `100 ms` suaviza mudanças de ativação e amplitude. Os valores são
demonstrativos.

Wow usa `85%` de componente irregular e `15%` periódica; flutter usa `90%` e
`10%`. Geradores e envelopes possuem sementes fixas independentes. Os sliders
controlam taxa característica e intensidade `Dry/Wet`, não uma frequência
senoidal pura.

## Tensão

```text
tension = tape_friction × (0.3 + 0.7 × abs(pwm))
```

O valor não tem unidade e não realimenta a planta.

## Animação

A RPM visual é convertida para velocidade angular:

```text
omega = rpm_visual × 2π / 60
```

O capstan usa `omega`; as bobinas usam fatores visuais de `0.6` e `0.9`. Esses
fatores não representam raios ou relações de transmissão reais.

Todos os ângulos são armazenados em graus e normalizados para a faixa de 0 a
menos de 360 graus após cada passo.

## Temporização

A interface solicita atualização a cada 16 ms, aproximadamente 60 vezes por
segundo. O tempo monotônico alimenta um scheduler que executa passos fixos de
`1 ms`. A recuperação é limitada a `100 ms`; o excedente é registrado no estado
e descartado.

O modelo não valida `dt`. Valores negativos ou exatamente iguais a `-tau` estão
fora do contrato atual e podem produzir resultados inválidos ou divisão por
zero.

## Limitações conhecidas

- Não há raio variável, inércia ou quantidade de fita por bobina.
- Não há acoplamento mecânico entre bobinas, fita e capstan.
- Não há encoder discreto nem perda de pulsos.
- Não há escorregamento, back-tension ou saturação física de torque.
- A tensão é apenas um indicador.
- A direção reversa ainda não existe.
- Os parâmetros não foram calibrados com dados experimentais.
- O controlador proporcional está sempre ativo; não existe comparação OFF/ON.
- Os perfis de wow e flutter são demonstrativos e aguardam revisão integrada.
- Não há reprodução de áudio ligada à velocidade da fita.

A evolução do núcleo está aprovada em
`docs/changes/digital-servo-foundations/`. A demonstração de áudio permanece em
`docs/changes/audible-digital-tach-demo/`.

Qualquer mudança nas equações ou no significado das variáveis deve começar por
um delta aprovado e, ao ser concluída, atualizar este documento e as specs
afetadas.
