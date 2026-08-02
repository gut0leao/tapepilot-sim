# Changelog

Todas as mudanças relevantes do projeto serão registradas neste arquivo. O
formato segue os princípios de Keep a Changelog; o projeto ainda não possui uma
versão estável publicada.

## Unreleased

### Added

- Documentação de arquitetura, desenvolvimento e modelo da simulação.
- Processo híbrido com ADRs e especificações.
- Glossário e guia de contribuição.
- Metadados e dependências em `pyproject.toml`.
- Núcleo de simulação importável sem Qt.
- Testes de caracterização do comportamento atual.
- Verificação automática de documentação e testes.
- Specs vivas por capacidade e processo de mudanças baseado em deltas.
- Guia mínimo para backlog, GitHub Project e sprints.
- GitHub Project configurado e backlog inicial criado a partir do roadmap.
- Visão de produto orientada à demonstração audível do servo digital.
- Change e épico para comparação Digital Tach OFF/ON.
- Perturbações episódicas e reproduzíveis de wow e flutter.
- Encoder discreto com jitter, perda de pulsos, dropout e filtragem.
- Servo digital PI/PID com transição suave, anti-windup e fallback.
- Métrica de erro RMS móvel e referências visuais de desempenho.
- Executor de cenários de integração headless com relatórios JSON e CSV.

### Changed

- O relógio da interface passou a usar fonte monotônica.
- SVGs recebem dimensões visuais explícitas.
- GitHub Actions oficiais atualizadas para versões baseadas em Node.js 24.
- Diagramas da documentação foram padronizados em Mermaid.
- Estado, controlador proporcional, planta, falhas e encoder visual foram
  separados em módulos, preservando o comportamento do protótipo.
- Scheduler fixo e perfis parametrizáveis de wow/flutter foram incorporados ao
  núcleo.
- Ruído colorido, envelope variável e controles Dry/Wet foram adicionados às
  perturbações de wow e flutter.
- O núcleo passou a executar em passos fixos de 1 ms, independente da taxa de
  atualização da interface.
- A change de fundamentos do servo digital foi validada, incorporada às specs
  vigentes e arquivada.

### Fixed

- Caminho do arquivo SVG do capstan.
