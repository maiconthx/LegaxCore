# Checklist de release LegaxCore

## Exigencias de CI
- [ ] Baseline e licenca preservados
- [ ] PHPStan e PHPUnit passaram
- [ ] Testes de integracao `tests/travis.sh` passaram
- [ ] `LegaxCore.phar` foi gerado e aberto como PHAR
- [ ] SHA-256 conferido

## Homologacao manual obrigatoria
- [ ] Login/logout com Minecraft Bedrock 1.26.30
- [ ] Carregamento de chunks e mundos, salvamento e reinicio
- [ ] Inventarios, transacoes e entidades
- [ ] BedWars, SkyWars, lobby, grupos, economia e estatisticas
- [ ] Testes em copia dos mundos (nunca sobre o unico backup)
- [ ] PHP e plugins registrados com versoes precisas
- [ ] Release permanece draft ate aprovacao explicita

## Plano de rollback
1. Pare o servidor e suspenda novas gravacoes.
2. Salve logs e dados de diagnostico.
3. Restaure PHAR antigo e os dados do backup correspondente.
4. Abra issue e crie um teste de regressao para a falha.

**Aviso:** a Fase 1 ainda usa protocolo original 1.26.30; nao anuncia compatibilidade com Bedrock 1.26.50 ou superior.
