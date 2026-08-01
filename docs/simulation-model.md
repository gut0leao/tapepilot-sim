# Modelo da simulação

## Propósito e validade

O modelo atual existe para demonstrar o loop de controle e sua visualização. Ele
é qualitativo: os valores não foram identificados a partir de um mecanismo real
e não devem ser usados como previsões físicas.

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
`docs/specs/reverse-transport/`.

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

A interface solicita um passo a cada 16 ms, aproximadamente 60 vezes por
segundo. O modelo usa o `dt` realmente medido por `time.monotonic()`, portanto a
evolução acompanha atrasos da interface em vez de assumir um passo fixo.

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

Qualquer mudança nas equações ou no significado das variáveis deve atualizar
este documento e possuir uma spec quando alterar o comportamento observável.
