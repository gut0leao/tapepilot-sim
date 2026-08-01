# Design: injeção de falhas

Os sliders pertencem à interface e escrevem valores normalizados em `SimState`
a cada tick. O modelo calcula atrito e tensão deterministicamente; o jitter usa
`random.gauss(0, 1)` e é aplicado depois da atualização da RPM da planta.

O termo “encoder jitter” representa intenção futura. Não existe ainda um
componente de encoder.

