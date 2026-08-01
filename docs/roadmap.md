# Roadmap

O roadmap registra direção e prioridade, não datas prometidas. Os itens marcados
como concluídos descrevem o protótipo atual.

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
- [ ] Implementar o sentido reverso de `REW`

## 3. Controle de velocidade

- [ ] Definir uma interface para controladores
- [ ] Implementar PID
- [ ] Permitir ajuste de `Kp`, `Ki` e `Kd`
- [ ] Medir overshoot e tempo de acomodação
- [ ] Modelar saturação do atuador

## 4. Encoder e falhas

- [ ] Modelar pulsos discretos do encoder
- [ ] Aplicar ruído à medição realimentada
- [ ] Simular perda de pulsos e dropout
- [ ] Simular escorregamento da fita

## 5. Modelo mecânico

- [ ] Modelar raio variável das bobinas
- [ ] Modelar inércia rotacional
- [ ] Modelar back-tension
- [ ] Acoplar tensão, bobinas e capstan
- [ ] Validar parâmetros com medições reais

## 6. Integração com hardware

- [ ] Definir interface de comunicação
- [ ] Exportar parâmetros do controlador
- [ ] Reproduzir entradas registradas em hardware
- [ ] Comparar simulação e medições reais

Antes de implementar um item que altere comportamento, deve-se criar ou aprovar
sua especificação em `docs/specs/`.
