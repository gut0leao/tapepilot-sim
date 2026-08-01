# Design: modos de transporte

`MainWindow` conecta cada botão a `Simulator.set_transport(mode)`. O estado
armazena a string selecionada e `Simulator.step(dt)` resolve o setpoint por uma
ramificação simples. `FF` e `REW` compartilham atualmente o mesmo ramo positivo.

A mudança de sentido proposta para `REW` está em
`docs/changes/reverse-transport/`.

