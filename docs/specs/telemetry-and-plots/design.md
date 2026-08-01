# Design: telemetria e gráficos

`MainWindow` mantém listas paralelas para tempo, setpoint, RPM, PWM, erro e
tensão. Depois de inserir uma amostra, remove o primeiro elemento de cada lista
enquanto a janela exceder 20 segundos.

Os quatro `PlotWidget` usam proporções horizontais 2:1:1:1. O gráfico de RPM
possui duas curvas; os demais possuem uma curva cada.

