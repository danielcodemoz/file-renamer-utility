# Normalizar nomes de ficheiros

**Demo ao vivo:** [https://danielcodemoz.github.io/file-renamer-utility/](https://danielcodemoz.github.io/file-renamer-utility/)

Laboratório de Daniel Marcos (Maputo) — não é um produto de cliente. Pré-visualiza e aplica regras combináveis aos nomes de ficheiros: slugify, procurar/substituir, numeração `001`, `002`…, maiúsculas/minúsculas, prefixo, sufixo e extensão.

## Ferramenta web

Cola uma lista de nomes ou escolhe ficheiros no browser. **Só se lê o nome** — o conteúdo nunca é carregado nem enviado.

- Modos combináveis (barra de opções)
- Contagem de ficheiros e de nomes que realmente mudam
- Tabela original | novo | estado
- Copiar nomes novos
- Descarregar o mapeamento em TSV/txt (`original` + tab + `novo`)
- Estado vazio e botão de exemplos

## CLI (Python)

O script `file_renamer.py` aplica as mesmas regras e **renomeia de verdade** os ficheiros duma pasta. Usa `--simular` para ver o mapeamento sem escrever.

```bash
python file_renamer.py --help
python file_renamer.py ./fotos --simular
python file_renamer.py ./docs --prefixo 2026_ --numeracao --sufixo _v1
python file_renamer.py ./docs --procurar " " --substituir _ --caso minusculas --manter-ext
```

- Portfólio: [danielpro.dev](https://danielpro.dev)
- Código: [github.com/danielcodemoz/file-renamer-utility](https://github.com/danielcodemoz/file-renamer-utility)

Autor: Daniel Marcos, Maputo.
