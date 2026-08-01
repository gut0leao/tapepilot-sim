# Design: controle de velocidade

O protótipo usa um controlador proporcional dentro de `Simulator.step()`. A
planta é uma interpolação de primeira ordem dependente do `dt` medido. Controle
e planta permanecem no mesmo módulo, mas não dependem de Qt.

A separação futura em `controller.py` e `plant.py` deve preservar estes
requisitos ou ser precedida por um delta aprovado.

