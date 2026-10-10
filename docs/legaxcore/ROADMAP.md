# Roadmap do LegaxCore

## Fase 1: baseline reproduzivel
- [x] Criar branches baseadas na tag 5.44.3, sem modificar `stable` original
- [x] Criar arquivos de CI, verificacao, guia de release e manifesto de compatibilidade
- [ ] Validar os jobs do GitHub Actions (PHPStan, PHPUnit, integracao, PHAR)
- [ ] Mesclar PR na linha `legaxcore/stable` apos revisao
- [ ] Validar login Bedrock 1.26.30 com clientes e plugins reais

## Fase 2: forks independentes
- [ ] Criar forks de BedrockProtocol, BedrockData e schemas de upgrade preservando licencas
- [ ] Fixar versoes no Composer e testar caminhos de override
- [ ] Adicionar testes de serializacao e pacotes

## Fase 3: Bedrock futuro
- [ ] Monitorar as alteracoes publicas documentadas pela Mojang
- [ ] Implementar mudancas em pacotes, componentes, blocos, itens e schemas
- [ ] Testar login, inventarios, chunk/world, entidades e API de plugins
- [ ] Anunciar suporte somente apos homologacao real

## Fase 4: Legax Network
- [ ] Validar BedWars, SkyWars, lobby, party, economia e estatisticas
- [ ] Proteger mundos e registros com backups, migracoes e rollback
- [ ] Definir releases verificadas e fluxo de deploy seguro

## Regras
- Preservar namespaces `pocketmine\\` na Fase 1
- Sem deploy automatico em producao
- Manter `stable` original imutavel; branch propria e `legaxcore/stable`
