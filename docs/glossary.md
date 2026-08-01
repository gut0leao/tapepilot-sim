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

## Controlador embarcado

Dispositivo que executará medição, controle e atuação no equipamento real. O
termo permanece independente de ESP32, Raspberry Pi Pico ou outra plataforma.

## Digital Tach

Nome de interface para o sistema digital de realimentação de velocidade. Em
`OFF`, a planta recebe comando nominal sem PID; em `ON`, encoder e PID fecham a
malha de controle.

## Dropout do encoder

Intervalo em que pulsos esperados do encoder não são observados.

## Jitter do encoder

Variação aleatória no instante ou na estimativa dos pulsos. Atualmente, o
TapePilot aplica ruído apenas à animação, não à realimentação do controlador.

## Flutter

Variação relativamente rápida da velocidade física da fita, percebida como
modulação rápida de pitch e tempo.

## Malha aberta

Operação sem correção baseada na medição de saída. Na demonstração proposta,
corresponde a `Digital Tach OFF`.

## Malha fechada

Operação em que a velocidade medida realimenta o controlador. Na demonstração
proposta, corresponde a `Digital Tach ON`.

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

## Velocidade física da fita

Saída da planta que determina o movimento e a taxa de reprodução do áudio. É
distinta da medição do encoder e do comando aplicado ao atuador.

## Wow

Variação relativamente lenta da velocidade física da fita, percebida como
oscilação lenta de afinação e tempo.
