# Visualização mecânica

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir a representação visual e o movimento dos componentes mecânicos.

## Escopo

- Duas bobinas e um capstan em SVG.
- Escala, posição, pivô e rotação.
- Conversão da RPM visual em ângulos.

## Fora de escopo

- Fidelidade mecânica, caminho da fita e pinch roller.
- Telemetria e gráficos.

## Requisitos funcionais

- **MV-RF-01:** A cena deve carregar `reel_left.svg`, `reel_right.svg` e
  `capstan.svg` a partir de `assets/svg/`.
- **MV-RF-02:** Cada bobina deve ter largura visual de 180 px.
- **MV-RF-03:** O capstan deve ter largura visual de 70 px.
- **MV-RF-04:** A proporção original de cada SVG deve ser preservada.
- **MV-RF-05:** Cada peça deve girar em torno do centro de seu `boundingRect`.
- **MV-RF-06:** O capstan deve usar a velocidade angular visual; as bobinas
  esquerda e direita devem usar fatores 0.6 e 0.9.
- **MV-RF-07:** Os ângulos devem ser expressos em graus e normalizados módulo
  360.

## Requisitos não funcionais

- **MV-RNF-01:** A cena deve reservar altura mínima de 360 px.
- **MV-RNF-02:** O carregamento vigente pode depender da raiz do repositório.

## Critérios de aceitação

### MV-CA-01: carregamento

- **Dado** que a aplicação é iniciada na raiz do projeto;
- **Quando** a janela abre;
- **Então** as duas bobinas e o capstan devem aparecer nas dimensões definidas.

### MV-CA-02: movimento

- **Dado** um modo com RPM positiva;
- **Quando** a simulação executa um passo;
- **Então** os três ângulos devem avançar no sentido positivo.

## Limitações vigentes

- Posições e escalas estão fixas no código.
- Os fatores angulares não representam relações físicas.
- Não há fita, pinch roller ou redimensionamento responsivo da cena.

## Evidências

- **Código:** `app.py`, `sim/model.py`, `assets/svg/`.
- **Testes:** `test_angles_advance_in_current_positive_direction` cobre
  `MV-RF-06` parcialmente.
- **Validação manual:** presença, escala e rotação validadas em 2026-07-31.

