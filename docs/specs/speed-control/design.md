# Design: controle de velocidade

O simulador usa `DigitalServoController`, em `sim/controller.py`, e
`FirstOrderPlant`, em `sim/plant.py`. `Simulator.step()` permanece como fachada
e coordena controlador, encoder e planta. Nenhum deles depende de Qt.

Em `Digital Tach OFF`, o controlador entrega o comando nominal. Em `ON`, o PID
atua sobre a RPM filtrada, com saturação, anti-windup, transferência suave e
fallback durante dropout. O contrato observável vigente está em
[`spec.md`](spec.md); as decisões completas permanecem na
[change arquivada](../../changes/archive/2026-08-01-digital-servo-foundations/design.md).
