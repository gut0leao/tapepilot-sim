# Roadmap

O roadmap registra a sequência estratégica, não datas, prioridade operacional
ou compromisso de sprint. Esses dados permanecem no GitHub Project.

## Resultado central

[Épico #10 — Demonstrar estabilização audível do servo digital](https://github.com/gut0leao/tapepilot-sim/issues/10).

Demonstrar que um controlador digital reduz variações físicas da fita por meio
de áudio, gráficos e métricas, comparando a mesma perturbação com `Digital Tach
OFF` e `ON`.

## 1. Baseline concluído

- [x] Interface Qt e controles de transporte.
- [x] Animação em SVG.
- [x] Modelo qualitativo de primeira ordem.
- [x] Controle proporcional.
- [x] Gráficos e falhas demonstrativas.
- [x] Núcleo testável sem Qt.
- [x] Specs vivas, changes, Issues e Project.

## 2. Fundamentos do servo digital

- [ ] [Separar planta, controlador, encoder e falhas](https://github.com/gut0leao/tapepilot-sim/issues/4).
- [ ] [Modelar distúrbios reproduzíveis de wow e flutter](https://github.com/gut0leao/tapepilot-sim/issues/12).
- [ ] [Modelar encoder discreto e falhas de sinal](https://github.com/gut0leao/tapepilot-sim/issues/5).
- [ ] [Implementar controlador PID ajustável](https://github.com/gut0leao/tapepilot-sim/issues/7).
- [x] Definir unidades, limites do atuador e taxas de amostragem no design da
  change do épico #10.

## 3. Demonstração audível

- [ ] [Tornar caminhos dos assets independentes da execução](https://github.com/gut0leao/tapepilot-sim/issues/6).
- [ ] [Reproduzir áudio conforme a velocidade física da fita](https://github.com/gut0leao/tapepilot-sim/issues/11).
- [ ] [Adicionar comparação Digital Tach OFF/ON e métricas](https://github.com/gut0leao/tapepilot-sim/issues/13).
- [ ] Validar com amostras sustentadas de voz ou cordas.
- [ ] Comparar execuções com a mesma perturbação.

## 4. Qualidade e manutenção do simulador

- [ ] [Ampliar testes da interface e do runtime](https://github.com/gut0leao/tapepilot-sim/issues/8).
- [ ] [Implementar o sentido reverso de `REW`](https://github.com/gut0leao/tapepilot-sim/issues/9).

## 5. Fidelidade e validação física

- [ ] [Evoluir o modelo mecânico de fita e bobinas](https://github.com/gut0leao/tapepilot-sim/issues/3).
- [ ] Caracterizar sensor, motor, atuador, inércia e cargas de um mecanismo real.
- [ ] Ajustar a planta simulada com dados medidos.
- [ ] Comparar resposta simulada e resposta real.

## 6. Controlador embarcado

- [ ] [Preparar integração com hardware embarcado](https://github.com/gut0leao/tapepilot-sim/issues/2).
- [ ] Definir requisitos elétricos, temporais e de segurança.
- [ ] Escolher a plataforma somente depois desses requisitos.
- [ ] Exportar e validar o controlador no hardware.
- [ ] Avaliar compatibilidade com equipamentos alvo.

Antes de implementar comportamento novo, deve-se aprovar sua change. Depois da
validação, o delta é incorporado às specs vigentes e a change é arquivada.
