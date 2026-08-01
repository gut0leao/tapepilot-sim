# Roadmap

O roadmap registra direção e prioridade, não datas prometidas. Os itens marcados
como concluídos descrevem o protótipo atual.

Itens já promovidos ao product backlog possuem link para a Issue correspondente.
Prioridade, sprint e status são mantidos somente no GitHub Project.

## 1. Protótipo visual

- [x] Janela Qt
- [x] Botões de transporte
- [x] Animação com SVGs
- [x] Modelo de primeira ordem
- [x] Controle proporcional
- [x] Gráficos em tempo real
- [x] Sliders de atrito e jitter
- [x] Escala explícita dos SVGs

## 2. Base testável

- [x] Declarar dependências em arquivo versionado
- [x] Separar o núcleo da simulação da interface
- [x] Criar testes de caracterização do modelo
- [x] Adotar relógio monotônico
- [ ] Definir unidades e faixas dos parâmetros
- [ ] [Implementar o sentido reverso de `REW`](https://github.com/gut0leao/tapepilot-sim/issues/9)
- [ ] [Tornar caminhos dos assets independentes do diretório de execução](https://github.com/gut0leao/tapepilot-sim/issues/6)
- [ ] [Ampliar testes da interface e do runtime](https://github.com/gut0leao/tapepilot-sim/issues/8)

## 3. Controle de velocidade

- [ ] [Separar planta, controlador, encoder e falhas](https://github.com/gut0leao/tapepilot-sim/issues/4)
- [ ] [Implementar PID](https://github.com/gut0leao/tapepilot-sim/issues/7)
- [ ] Permitir ajuste de `Kp`, `Ki` e `Kd`
- [ ] Medir overshoot e tempo de acomodação
- [ ] Modelar saturação do atuador

## 4. Encoder e falhas

- [ ] [Modelar encoder discreto e falhas de sinal](https://github.com/gut0leao/tapepilot-sim/issues/5)
- [ ] Aplicar ruído à medição realimentada
- [ ] Simular perda de pulsos e dropout
- [ ] Simular escorregamento da fita

## 5. Modelo mecânico

Backlog: [Issue #3](https://github.com/gut0leao/tapepilot-sim/issues/3).

- [ ] Modelar raio variável das bobinas
- [ ] Modelar inércia rotacional
- [ ] Modelar back-tension
- [ ] Acoplar tensão, bobinas e capstan
- [ ] Validar parâmetros com medições reais

## 6. Integração com hardware

Backlog: [Issue #2](https://github.com/gut0leao/tapepilot-sim/issues/2).

- [ ] Definir interface de comunicação
- [ ] Exportar parâmetros do controlador
- [ ] Reproduzir entradas registradas em hardware
- [ ] Comparar simulação e medições reais

Antes de implementar um item que altere comportamento, deve-se aprovar sua
proposta e delta em `docs/changes/`. Depois da validação, o delta é incorporado
às specs vigentes.
