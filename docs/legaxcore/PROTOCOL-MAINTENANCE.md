# Protocolo Bedrock — Plano de manutencao independente

## Estado atual

LegaxCore se baseia em PMMP 5.44.3. O arquivo `legaxcore/dependency-pins.json` registra os 4 pacotes de Bedrock e respectivos **commits exatos do composer.lock**.

A camada de protocolo e bibliotecas `pocketmine/*` continuam originais nesta fase. **Nao foi criada nenhuma biblioteca independente ainda**, nem alterado `composer.json`.

## Repositorios a criar, preservando licencas/historico

| Futuro repo | Upstream (origem do composer.lock) | Nome do pacote Composer a preservar |
| --- | --- | --- |
| LegaxProtocol | pmmp/BedrockProtocol | pocketmine/bedrock-protocol |
| LegaxData | pmmp/BedrockData | pocketmine/bedrock-data |
| LegaxBlockSchema | pmmp/BedrockBlockUpgradeSchema | pocketmine/bedrock-block-upgrade-schema |
| LegaxItemSchema | pmmp/BedrockItemUpgradeSchema | pocketmine/bedrock-item-upgrade-schema |

Se quiser forks reais sob `maiconthx`, crie-os no GitHub. O atual conector possui escrita em repositorios existentes, **mas nao cria repositorios novos**. Nao crie uma pasta com o nome de uma biblioteca e a trate como fork.

Cada fork deve partir do commit declarado no manifesto para reproduzir a dependencia original. Commits posteriores exigem analise individual. Alguns projetos foram arquivados, outros podem ter manutencao fora de `pmmp`.

## Ordem segura para substituir bibliotecas

1. Criar os forks com as licencas originais e conferir os hashes no manifesto.
2. Em branch de teste do LegaxCore, configurar repositórios Composer do tipo VCS apontando para forks **existentes**.
3. Manter inicialmente os nomes dos pacotes Composer originais; mudar URLs nao significa alterar namespaces `pocketmine\\`.
4. Criar tags ou aliases Comp​oser compativeis com os requisitos do `composer.json`, sem simular uma versao do jogo que ainda nao funciona.
5. Rodar `composer update pocketmine/bedrock-protocol ... --with-dependencies` com revisao do diff de `composer.lock` e `composer install`; nunca usar `--ignore-platform-reqs` para validacao real.
6. Atualizar `dependency-pins.json` intencionalmente **somente apos** fixar e testar cada commit; isso libera o verificador.
7. Testar protocolo binario (roundtrips, pacotes e enums), data, conversoes, mundo, inventario e rede com cliente legitimo.
8. Gerar release candidata, com testes de plugins, antes de homologar em producao.

## Automacao de anuncios

`.github/workflows/legax-bedrock-watch.yml` consulta a ultima GitHub Release de
`Mojang/bedrock-protocol-docs` e abre uma **issue unica por tag**.

**Importante:** GitHub Actions executa workflows com agendamento a partir da **branch padrao**. Enquanto `stable` for a default, o monitor da nossa linha `legaxcore/stable` nao funcionara diariamente. Nao substitua a default sem antes conferir os workflows e configurar as permissoes do repositorio. Este monitor nao adapta pacotes automaticamente.

Documentacao da Mojang: https://github.com/Mojang/bedrock-protocol-docs
A documentacao possui termos proprios: referencia-la ou comparar metadados nao concede permissao irrestrita para redistribuir os JSONs.

## Habilitacao obrigatoria no GitHub

1. Em `https://github.com/maiconthx/LegaxCore/settings` ative **Issues** em Settings → General → Features.
2. Confira `legaxcore/stable` e os workflows antes de mudar a branch padrao de `stable` para `legaxcore/stable`.
3. Confirme que o Action possui `issues: write`, execute o monitor e verifique que cria apenas uma issue para cada nova tag.
4. Nao desative o erro de configuracao: o workflow falha explicitamente se Issues estiver desligado, para evitar falsa impressao de monitoramento ativo.

