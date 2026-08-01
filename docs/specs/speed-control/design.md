# Design: controle de velocidade

O protótipo usa `ProportionalController`, em `sim/controller.py`, e
`FirstOrderPlant`, em `sim/plant.py`. `Simulator.step()` permanece como fachada,
calcula o erro e coordena os dois componentes. Nenhum deles depende de Qt.

A extração preserva o controle proporcional e a interpolação de primeira ordem
vigentes. A evolução para atuador efetivo e PID está aprovada na change
`digital-servo-foundations`, mas ainda não representa o AS-IS.
