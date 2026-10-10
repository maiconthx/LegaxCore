# LegaxCore 0.1.0 — Fase 1

Fork independente em preparação, derivado de [PocketMine-MP 5.44.3](https://github.com/pmmp/PocketMine-MP/tree/5.44.3).

> **Estado:** baseline e testes. O código, o nome interno e a API 5 continuam os do PocketMine-MP 5.44.3. O artefato recebe o nome `LegaxCore.phar`, mas a engine **ainda não oferece suporte novo** ao Bedrock além de 1.26.30.

## Origem e licença

A origem é `pmmp/PocketMine-MP`, tag `5.44.3`. O histórico, os créditos e a licença LGPL-3.0 foram preservados. Este projeto não é afiliado à Mojang nem à equipe original do PocketMine-MP.

## Estratégia de branches

- `stable`: branch herdada do fork original. **Não será alterada neste PR.**
- `legaxcore/stable`: linha de manutenção própria, iniciada da tag `5.44.3`.
- `legaxcore/setup-v0.1.0`: proposta de configuração inicial.

Trabalhe em branches e abra PRs para `legaxcore/stable`. Não misture a branch `stable` do upstream com a nossa baseline 5.44.3.

## Compilação

O CI usa o binário PHP 8.2 do PMMP para Linux x86_64, com SHA-256 fixado. Para testes locais é necessário PHP com as extensões do PocketMine e Composer:

```bash
composer install --prefer-dist --no-interaction
./vendor/bin/phpstan analyze --no-progress --memory-limit=2G
./vendor/bin/phpunit --bootstrap vendor/autoload.php --fail-on-warning tests/phpunit
bash tests/travis.sh -t4
```

Para criar o PHAR após instalar dependências de produção:

```bash
composer install --no-dev --classmap-authoritative --prefer-dist
php -dphar.readonly=0 build/server-phar.php --out=LegaxCore.phar
sha256sum LegaxCore.phar > LegaxCore.phar.sha256
```

**Atenção:** os testes oficiais `tests/travis.sh` compilam `PocketMine-MP.phar` por conta própria. Nunca interprete sua aprovação isolada como prova de compatibilidade com cliente Bedrock mais novo.

## GitHub Actions e releases

O workflow `.github/workflows/legax-ci.yml` faz validação, PHPStan, PHPUnit, integração e gera um artefato de teste. As automações de publicação e sincronização herdadas do PMMP foram removidas da linha LegaxCore para evitar disparos involuntários. Depois dos testes e revisões, uma tag `v*` pode gerar **apenas um rascunho** de release; o jogo e plugins precisam de homologação manual.

**Não publique em produção nesta fase**. Guarde mundos, players, segredos, configurações pessoais e backups fora deste repositório.

Veja `docs/legaxcore/ROADMAP.md` e `docs/legaxcore/RELEASE-CHECKLIST.md`.
