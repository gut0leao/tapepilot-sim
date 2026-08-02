# Modelo da simulação

## Propósito e validade

O modelo atual existe para demonstrar o loop de controle e sua visualização. Ele
é qualitativo: os valores não foram identificados a partir de um mecanismo real
e não devem ser usados como previsões físicas.

`Simulator`, em `sim/model.py`, coordena componentes separados para estado,
controle digital, planta de primeira ordem, falhas e encoder discreto.

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
| `encoder_pulse_loss` | probabilidade de perda por pulso | 0 a 1 |
| `encoder_dropout` | descarte total de pulsos | booleano |
| `encoder_pulse_count` | pulsos aceitos acumulados | inteiro |
| `encoder_rpm_raw` | velocidade quantizada estimada pelo encoder | RPM |
| `encoder_rpm_filtered` | medição após passa-baixas de `50 ms` | RPM |
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

## Controle digital

Em `Digital Tach OFF`, a planta recebe comando nominal em malha aberta:

```text
command_nominal = rpm_setpoint / 3000
```

Em `ON`, um PID usa `encoder_rpm_filtered` e soma sua correção ao nominal. Os
ganhos iniciais são `Kp=0,001`, `Ki=0,002` e `Kd=0`. A derivada atua sobre
a medição e usa o intervalo real entre janelas de encoder, normalmente `10 ms`;
seu valor é mantido entre amostras. A integral é condicional durante saturação e
o comando final fica em `[-1,+1]`. Transições usam bias linear de `250 ms`.

Dropout durante `ON` ativa `FALLBACK`: a correção é retirada em `250 ms` e o
comando retorna ao nominal. Quando o sinal retorna, o PID reentra sem salto.

### Benchmark provisório

O benchmark do projeto mede a RPM física durante `5 s`, depois de `3 s` de
estabilização, em `PLAY` com wow contínuo de `0,5 Hz/1%` e demais falhas
desligadas. A meta provisória é RMS de até `1,8 RPM` (`0,1%`); até `3,6 RPM`
(`0,2%`) ainda é aceitável. Com `Kd = 0`, a execução automatizada obteve
aproximadamente `1,47 RPM` (`0,0815%`), atingindo a meta sem saturação. Esses
valores não constituem validação em hardware.

O cenário adicional de estresse usa todos os parâmetros de wow no máximo. Com
os ganhos padrão, sua primeira janela completa após estabilização produz cerca
de `0,255%`, sem saturação. Seu limite de regressão é `0,5%`; as metas
profissionais de `0,1%/0,2%` continuam restritas ao benchmark padrão.

`RollingRmsError`, em `sim/metrics.py`, executa essa medição no núcleo. A métrica
é reiniciada a cada mudança de setpoint, Digital Tach, ganho, falha ou parâmetro
de wow/flutter. Ela retorna indisponível durante os `3 s` de estabilização e
mantém uma janela móvel de `5 s`. O gráfico mostra o RMS percentual e referências
horizontais em `0,1%` e `0,2%`.

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
target = max(command_applied, 0) × 3000
target = target - friction_load × abs(command_applied)
target = max(target, 0)
```

Essa fórmula é uma heurística e não uma equação mecânica. O limite inferior em
zero também impede, no estado atual, a representação do sentido reverso.

## Encoder discreto

O encoder gera `100 pulsos/revolução`. Frações são acumuladas a cada passo e a
medição é atualizada em janelas de `10 ms`:

```text
encoder_rpm_raw = window_pulses × 60 / (100 × window_seconds)
jitter = normal(μ=0, σ=1) × encoder_jitter × 20 RPM
```

Perda de pulsos entre `0%` e `100%` é aplicada individualmente; dropout descarta
todos os pulsos. A sequência pseudoaleatória usa semente `3301`. Um filtro
passa-baixas de primeira ordem com constante de `50 ms` reduz os degraus de
`60 RPM`. As medições bruta e filtrada são observáveis. A animação usa `rpm`
física; em `Digital Tach ON`, o PID usa a RPM filtrada.

## Wow e flutter

A implementação combina ruído filtrado, envelope variável e uma
pequena senoide residual para modular o alvo físico da planta. Wow usa padrão
`0,5 Hz`, `1%` e episódios médios de `3 s`; flutter, `8 Hz`, `0,3%` e
episódios médios de `0,5 s`.
Cada componente possui ocorrência, duração, taxa característica e intensidade
independentes. Ocorrência representa a proporção média de tempo ativo; duração
representa o tamanho médio do episódio. Episódios ativos e intervalos inativos
variam entre `50%` e `150%` de seus valores médios. Se ambos estiverem ativos,
seus sinais são somados sem criar um estado adicional. Uma rampa de `100 ms`
suaviza o início, o fim e as mudanças de amplitude. Os valores são
demonstrativos.

Wow usa `85%` de componente irregular e `15%` periódica; flutter usa `90%` e
`10%`. Geradores e envelopes possuem sementes fixas independentes. Os sliders
controlam taxa característica e intensidade `Dry/Wet`, não uma frequência
senoidal pura. Geradores determinísticos separados controlam os episódios.

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
- A medição filtrada realimenta somente o modo `Digital Tach ON`.
- Não há escorregamento, back-tension ou saturação física de torque.
- A tensão é apenas um indicador.
- A direção reversa ainda não existe.
- Os parâmetros não foram calibrados com dados experimentais; essa calibração
  está registrada na Issue [#14](https://github.com/gut0leao/tapepilot-sim/issues/14).
- Os ganhos e parâmetros do controlador não foram calibrados em hardware.
- Os perfis de wow e flutter são demonstrativos e aguardam calibração física.
- Não há reprodução de áudio ligada à velocidade da fita.

O histórico da evolução do núcleo está arquivado em
`docs/changes/archive/2026-08-01-digital-servo-foundations/`. A demonstração de
áudio permanece proposta em `docs/changes/audible-digital-tach-demo/`.

Qualquer mudança nas equações ou no significado das variáveis deve começar por
um delta aprovado e, ao ser concluída, atualizar este documento e as specs
afetadas.
