# Guia de uso

## Iniciando

Execute `python3 app.py` na raiz do repositório. A aplicação abre uma janela de
1200 × 700 px intitulada “TapePilot V1 - Simulador (WSL/Qt/SVG)”.

A tela é dividida em:

- faixa fixa de telemetria no topo;
- cena mecânica com duas bobinas e um capstan;
- painel de transporte, falhas e telemetria;
- quatro gráficos na parte inferior.

## Controles de transporte

| Controle | Comportamento atual |
|---|---|
| `STOP` | define setpoint de 0 RPM |
| `PLAY` | define setpoint de 1800 RPM |
| `PAUSE` | define setpoint de 300 RPM |
| `FF` | define setpoint de 2600 RPM |
| `REW` | define setpoint de 2600 RPM |

`REW` ainda não inverte o sentido. Esse comportamento está registrado como
limitação e possui uma proposta de mudança em elaboração.

## Controle digital

`Digital Tach ON` fecha a malha usando a RPM filtrada do encoder. Os sliders
`Kp`, `Ki` e `Kd` alteram os ganhos durante a execução; os padrões demonstrativos
são respectivamente `0,001`, `0,002` e `0`. Em `OFF`, a planta usa apenas
o comando nominal correspondente ao setpoint.

O termo derivativo permanece disponível, mas inicia zerado porque, com o encoder
simulado atual, ele amplifica mais a quantização residual do que o wow físico.

As transições levam `250 ms` para evitar saltos. Se houver dropout com a chave
ligada, a telemetria mostra `FALLBACK` e a correção converge ao comando nominal.
Quando o sinal retorna, o PID é retomado suavemente.

Para comparação provisória, considere erro RMS de até `0,1%` como meta e até
`0,2%` como aceitável. Em `1800 RPM`, isso equivale a `1,8 RPM` e `3,6 RPM`.
Essas metas usam a RPM física e ainda aguardam calibração com hardware real.

## Injeção de falhas

Os sliders de falhas possuem valores inteiros de 0 a 100, convertidos
internamente para a faixa de 0 a 1.

### Atrito da fita

Reduz a velocidade-alvo e aumenta o indicador de tensão. O efeito é uma
heurística visual, sem unidade física.

### Jitter do encoder

Adiciona ruído gaussiano reproduzível, com escala de até `20 RPM`, à medição do
encoder. `Perda de pulsos` determina a probabilidade de descarte de cada pulso;
`Dropout do encoder` descarta todos os pulsos enquanto estiver marcado.

O encoder possui `100 pulsos/revolução` e atualiza sua estimativa a cada
`10 ms`. A RPM bruta evidencia os degraus de quantização; a RPM filtrada usa um
passa-baixas com constante de `50 ms`. Nesta etapa, suas falhas aparecem na
telemetria e nas curvas do encoder, mas não alteram planta, controlador,
animação ou curva física de RPM.

### Wow e flutter

Wow e flutter possuem sliders independentes. Quando os dois ocorrem ao mesmo
tempo, seus efeitos são somados naturalmente; não existe um estado `Combined` a
ser selecionado ou armazenado. `Restaurar padrão` zera a ocorrência de ambos e
recupera:

- wow em `0,5 Hz`, `1%` e duração média de `3 s`;
- flutter em `8 Hz`, `0,3%` e duração média de `0,5 s`.

`Taxa característica` controla a velocidade média das irregularidades.
`Intensidade — Dry ↔ Wet` controla quanto cada perturbação afeta a planta. Os
sliders de `Ocorrência média` determinam a proporção média do tempo com a
perturbação presente; em zero, o efeito permanece ausente. `Duração média`
controla o tamanho típico dos episódios. Episódios e intervalos variam
aleatoriamente em torno desses valores.

O sinal combina ruído filtrado dominante, presença variável e uma pequena
periodicidade residual. Wow e flutter usam sequências distintas, mas
reproduzíveis.

Esses perfis modulam a velocidade física simulada e são valores demonstrativos,
não medições de um equipamento real.

## Telemetria

A faixa fixa acima da cena mecânica mostra:

- modo de transporte;
- RPM simulada e setpoint;
- PWM e erro;
- estado `OFF`, `ON` ou `FALLBACK`, termos `P/I/D`, bias, comandos solicitado e
  aplicado, saturação e bloqueio da integral;
- erro RMS percentual ou indicação `estabilizando`;
- níveis de atrito e jitter;
- RPM bruta e filtrada, pulsos acumulados, perda e dropout do encoder;
- valores instantâneos de wow e flutter;
- tensão simulada.

O texto pode ser selecionado com o mouse.

## Gráficos

Os cinco gráficos são atualizados em tempo real e preservam os últimos 20 segundos:

- RPM desejada, física, bruta do encoder e filtrada do encoder;
- comandos solicitado e aplicado;
- erro de controle;
- tensão simulada.
- erro RMS percentual móvel.

O RMS descarta `3 s` depois de cada mudança de setpoint e usa uma janela móvel
de até `5 s`. Mudanças de Digital Tach, ganhos, falhas ou parâmetros de
wow/flutter também reiniciam a estabilização e a janela. A linha verde marca a
meta de `0,1%`; a vermelha, o limite provisório de `0,2%`. Em `STOP`, a métrica
fica indisponível.

As curvas possuem legendas e cores distintas. Os gráficos usam antialiasing
para melhorar a apresentação.

## Cena mecânica

As bobinas possuem largura visual de 180 px e o capstan, 70 px. As peças giram
em torno do centro de seus respectivos SVGs. Os fatores de velocidade são
apenas visuais e não representam relações mecânicas reais.

## Limitações de operação

- Parâmetros avançados da planta e do controlador não estão na interface.
- Não há persistência ou exportação de dados.
- Não há pausa do relógio da simulação; `PAUSE` é um modo de baixa velocidade.
- Não há indicação visual do botão atualmente selecionado.
- Os caminhos dos SVGs dependem da execução na raiz do projeto.
