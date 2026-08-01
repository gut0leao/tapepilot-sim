# Glossário

## Back-tension

Tensão aplicada no lado de alimentação para manter a fita estável. Ainda não é
modelada pelo TapePilot.

## Bobina de alimentação

Bobina da qual a fita sai durante a reprodução normal. Seu raio efetivo varia
com a quantidade de fita, efeito ainda não modelado.

## Bobina de recolhimento

Bobina que recebe a fita durante a reprodução normal.

## Capstan

Eixo que, em conjunto com o *pinch roller*, impõe a velocidade linear da fita.
No protótipo, sua rotação é apenas uma representação visual proporcional à RPM.

## Dropout do encoder

Intervalo em que pulsos esperados do encoder não são observados.

## Jitter do encoder

Variação aleatória no instante ou na estimativa dos pulsos. Atualmente, o
TapePilot aplica ruído apenas à animação, não à realimentação do controlador.

## Pinch roller

Rolete que pressiona a fita contra o capstan. Ainda não possui modelo próprio.

## Planta

Modelo do sistema físico controlado: motor, capstan, bobinas, fita e cargas.

## PWM

Comando normalizado enviado ao atuador. No modelo atual, varia de -1 a 1, sem
representar frequência, tensão ou ciclo de trabalho de hardware específico.

## RPM medida

Estimativa de velocidade fornecida pelo sensor. O protótipo ainda usa diretamente
a RPM interna da planta nos gráficos e no controle.

## Setpoint

Valor desejado para uma variável controlada. No TapePilot atual, representa a
RPM desejada para cada modo de transporte.

## Tensão da fita

Força longitudinal aplicada à fita. O valor atual é um indicador normalizado e
sem unidade física.

