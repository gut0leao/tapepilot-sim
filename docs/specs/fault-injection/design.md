# Design: injeção de falhas

Os sliders pertencem à interface e escrevem valores normalizados em `SimState`
a cada tick. `FaultModel`, em `sim/faults.py`, calcula atrito e tensão;
`VisualEncoder`, em `sim/encoder.py`, usa `random.gauss(0, 1)` depois da
atualização da RPM da planta.

Embora exista um componente separado, o termo “encoder jitter” ainda representa
intenção futura: a medição produzida é usada somente no movimento visual e não
fecha a malha.
