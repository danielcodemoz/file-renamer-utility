#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normaliza nomes de ficheiros — as mesmas regras da ferramenta web."""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata


def slugify_stem(stem: str) -> str:
    nfd = unicodedata.normalize("NFD", stem)
    sem_acentos = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    s = sem_acentos.lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9._-]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "ficheiro"


def title_case(value: str) -> str:
    def cap(match: re.Match[str]) -> str:
        word = match.group(0)
        return word[0].upper() + word[1:].lower() if word else word

    return re.sub(r"[^\s._-]+", cap, value)


def split_name(name: str) -> tuple[str, str]:
    i = name.rfind(".")
    if 0 < i < len(name) - 1:
        return name[:i], name[i:]
    return name, ""


def apply_name(name: str, opts: argparse.Namespace, index: int) -> str:
    work = name
    if opts.procurar:
        work = work.replace(opts.procurar, opts.substituir or "")

    stem, ext = split_name(work)

    if opts.slugify:
        stem = slugify_stem(stem)

    if opts.caso == "minusculas":
        stem = stem.lower()
    elif opts.caso == "maiusculas":
        stem = stem.upper()
    elif opts.caso == "titulo":
        stem = title_case(stem)

    numero = ""
    if opts.numeracao:
        n = opts.inicio + index
        numero = f"{n:0{opts.largura}d}_"

    if opts.ext_minusculas:
        ext = ext.lower()

    prefixo = opts.prefixo or ""
    sufixo = opts.sufixo or ""
    return f"{prefixo}{numero}{stem}{sufixo}{ext}"


def list_files(pasta: str) -> list[str]:
    nomes = []
    for nome in os.listdir(pasta):
        caminho = os.path.join(pasta, nome)
        if os.path.isfile(caminho):
            nomes.append(nome)
    nomes.sort()
    return nomes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file_renamer.py",
        add_help=False,
        usage="%(prog)s [opções] pasta",
        description=(
            "Renomeia ficheiros numa pasta com as mesmas regras da ferramenta web: "
            "slugify, procurar/substituir, numeração sequencial, maiúsculas/minúsculas, "
            "prefixo, sufixo e extensão."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "exemplos:\n"
            "  python file_renamer.py ./fotos --simular\n"
            "  python file_renamer.py ./docs --prefixo 2026_ --numeracao\n"
            "  python file_renamer.py ./docs --procurar \" \" --substituir _ --caso minusculas\n"
            "  python file_renamer.py ./docs --sem-slugify --caso titulo --manter-ext\n"
            "\n"
            "A ferramenta web (só pré-visualização, nunca envia bytes) está em:\n"
            "  https://danielcodemoz.github.io/file-renamer-utility/\n"
        ),
    )
    parser._positionals.title = "argumentos"
    parser._optionals.title = "opções"
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="mostrar esta ajuda e sair",
    )
    parser.add_argument(
        "pasta",
        help="Pasta cujos ficheiros serão (pré-)renomeados",
    )
    parser.add_argument(
        "--slugify",
        dest="slugify",
        action="store_true",
        default=True,
        help="Slugificar: minúsculas, sem acentos, espaços → _ (predefinição: ligado)",
    )
    parser.add_argument(
        "--sem-slugify",
        dest="slugify",
        action="store_false",
        help="Não slugificar o nome",
    )
    parser.add_argument(
        "--procurar",
        default="",
        metavar="TEXTO",
        help="Texto a procurar (substituição literal em todo o nome)",
    )
    parser.add_argument(
        "--substituir",
        default="",
        metavar="TEXTO",
        help="Texto de substituição (usar com --procurar)",
    )
    parser.add_argument(
        "--numeracao",
        action="store_true",
        help="Prefixar 001_, 002_, … (largura controlada por --largura)",
    )
    parser.add_argument(
        "--inicio",
        type=int,
        default=1,
        metavar="N",
        help="Primeiro número da sequência (predefinição: 1)",
    )
    parser.add_argument(
        "--largura",
        type=int,
        default=3,
        metavar="N",
        help="Algarismos com zeros à esquerda (predefinição: 3 → 001)",
    )
    parser.add_argument(
        "--caso",
        choices=("nenhum", "minusculas", "maiusculas", "titulo"),
        default="nenhum",
        help="Transformação de maiúsculas/minúsculas no nome (depois do slugify)",
    )
    parser.add_argument(
        "--prefixo",
        default="",
        metavar="TEXTO",
        help="Prefixo opcional antes do nome (e da numeração)",
    )
    parser.add_argument(
        "--sufixo",
        default="",
        metavar="TEXTO",
        help="Sufixo opcional no nome, antes da extensão",
    )
    ext = parser.add_mutually_exclusive_group()
    ext.add_argument(
        "--ext-minusculas",
        dest="ext_minusculas",
        action="store_true",
        default=True,
        help="Forçar a extensão em minúsculas (predefinição)",
    )
    ext.add_argument(
        "--manter-ext",
        dest="ext_minusculas",
        action="store_false",
        help="Manter a extensão original (ex.: .JPG)",
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Só mostrar o mapeamento; não renomear",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    opts = parser.parse_args(argv)

    pasta = os.path.abspath(opts.pasta)
    if not os.path.isdir(pasta):
        print(f"Erro: a pasta não existe: {pasta}", file=sys.stderr)
        return 1

    if opts.largura < 1:
        print("Erro: --largura deve ser ≥ 1.", file=sys.stderr)
        return 1

    ficheiros = list_files(pasta)
    if not ficheiros:
        print("Nenhum ficheiro nesta pasta.")
        return 0

    mapeamento: list[tuple[str, str]] = []
    for i, nome in enumerate(ficheiros):
        novo = apply_name(nome, opts, i)
        mapeamento.append((nome, novo))

    total = len(mapeamento)
    alterados = sum(1 for a, b in mapeamento if a != b)
    iguais = total - alterados

    print(f"Pasta: {pasta}")
    print(f"{total} ficheiros · {alterados} a alterar · {iguais} iguais")
    print("original\tnovo")
    for antigo, novo in mapeamento:
        marca = "ALTERA" if antigo != novo else "igual"
        print(f"{antigo}\t{novo}\t{marca}")

    if opts.simular:
        print("\nSimulação: nenhum ficheiro foi renomeado.")
        return 0

    if alterados == 0:
        print("\nNada a fazer.")
        return 0

    feitos = 0
    for antigo, novo in mapeamento:
        if antigo == novo:
            continue
        origem = os.path.join(pasta, antigo)
        destino = os.path.join(pasta, novo)
        if os.path.abspath(origem) == os.path.abspath(destino):
            continue
        if os.path.exists(destino):
            print(f"Aviso: a saltar «{antigo}» — o destino «{novo}» já existe.")
            continue
        os.rename(origem, destino)
        print(f"Renomeado: {antigo} → {novo}")
        feitos += 1

    print(f"\nConcluído. Ficheiros renomeados: {feitos}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
