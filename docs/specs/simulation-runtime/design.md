# Design: runtime da simulação

`app.py` contém apenas a apresentação e importa o núcleo por `from sim import
Simulator`. O pacote `sim` reexporta `SimState` e `Simulator` como API pública.

Um `QTimer` dispara `MainWindow.tick()`. Dois valores de `time.monotonic()`
mantêm o `dt` do modelo e o eixo de tempo dos gráficos.

A CI usa Ubuntu, Python 3.12 e actions compatíveis com Node.js 24.

