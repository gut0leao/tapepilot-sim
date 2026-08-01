# ADR 0003: Áudio como evidência do servo digital

- **Estado:** Aceito
- **Data:** 2026-08-01

## Contexto

Reproduzir áudio apenas quando o transporte está em `PLAY` não acrescenta valor
suficiente ao simulador. O objetivo relevante é perceber se um controlador
digital reduz variações físicas de velocidade que causam wow e flutter.

## Decisão

O TapePilot será orientado à demonstração e ao desenvolvimento de um servo
digital de velocidade. O áudio:

- acompanhará a velocidade física simulada da fita;
- não acompanhará diretamente a medição do encoder ou a saída do PID;
- será usado para comparar o controle digital desligado e ligado;
- complementará gráficos e métricas quantitativas;
- não será tratado como simulação completa da cadeia de áudio da fita.

Plataformas de hardware serão descritas genericamente como controlador embarcado
até que requisitos reais permitam uma escolha fundamentada.

## Consequências

### Positivas

- A demonstração se alinha ao valor pretendido do produto.
- Erros conceituais entre planta, sensor e áudio ficam explícitos.
- O PID pode ser avaliado auditiva e quantitativamente.
- O simulador prepara uma transição mais clara para hardware.

### Negativas

- A planta precisa ser separada do controlador e do encoder.
- Wow e flutter precisam de modelos reproduzíveis.
- Reprodução variável de áudio aumenta complexidade e requisitos de tempo real.
- Resultados simulados ainda exigem validação em mecanismos reais.

