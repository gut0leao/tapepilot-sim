# Tarefas: transporte reverso

As tarefas funcionais só devem entrar em execução depois que a spec for
aprovada. Preparações independentes que não alteram o comportamento podem ser
concluídas durante o estado `Draft`.

- [ ] Resolver as questões em aberto da spec.
- [ ] Alterar o estado da spec para `Approved`.
- [x] Extrair o simulador para um módulo testável sem Qt.
- [x] Criar testes que caracterizem os modos existentes.
- [ ] Alterar o setpoint de `REW` para -2600 RPM.
- [ ] Permitir RPM negativa na dinâmica.
- [ ] Tornar o atrito simétrico nos dois sentidos.
- [ ] Preservar o sinal no jitter e na animação.
- [ ] Testar as transições `STOP → REW`, `REW → STOP`, `FF → REW` e `REW → FF`.
- [ ] Validar visualmente bobinas, capstan, telemetria e gráficos.
- [ ] Atualizar `docs/simulation-model.md`.
- [ ] Registrar evidências de validação.
- [ ] Alterar o estado da spec para `Implemented`.
