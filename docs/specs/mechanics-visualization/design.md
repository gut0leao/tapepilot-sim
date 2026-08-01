# Design: visualização mecânica

A cena usa `QGraphicsScene`, `QGraphicsView` e três `QGraphicsSvgItem`. Uma
função local calcula `largura desejada / largura original` e aplica `setScale`.

As posições vigentes são `(60, 60)`, `(300, 60)` e `(200, 200)` para bobina
esquerda, bobina direita e capstan. A rotação é atualizada pela janela a partir
dos ângulos calculados no núcleo.

