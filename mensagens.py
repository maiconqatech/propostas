#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera as mensagens de primeiro contato ja com o link colado.

Le os <nicho>/_leads.csv (feitos pelo gerar.py) e escreve:
    <nicho>/_MENSAGENS.md   mensagem pronta por lead, pra copiar e colar
    _ENVIOS.csv             lista mestre: nicho;empresa;cidade;whatsapp;link;abrir;mensagem;status

A coluna "abrir" e um link wa.me: voce clica, o WhatsApp abre a conversa com
aquele numero e a mensagem ja digitada. Voce so revisa e envia.

Rodar:  python mensagens.py
"""
import csv, urllib.parse, pathlib

RAIZ = pathlib.Path(__file__).parent
NICHOS = ["odonto", "vet", "fisio", "pilates", "auto"]

SUBSTANTIVO = {
    "odonto": "pra clínica",
    "vet": "pra clínica",
    "fisio": "pra clínica",
    "pilates": "pro estúdio",
    "auto": "pro seu estúdio",
}


def mensagem(empresa: str, cidade: str, nota: str, tem_nota: bool, link: str, nicho: str) -> str:
    noun = SUBSTANTIVO[nicho]
    if tem_nota:
        l1 = f"Oi! Tudo bem? Achei a {empresa} aqui em {cidade} e reparei que vocês têm {nota} no Google, mas ainda não aparecem com um site próprio."
    else:
        l1 = f"Oi! Tudo bem? Achei a {empresa} aqui em {cidade} e vi que vocês ainda não têm um site próprio."
    return (
        f"{l1}\n\n"
        f"Montei uma prévia de site {noun}, só pra te mostrar uma ideia, já com as informações de vocês dentro: {link}\n\n"
        f"Dá uma olhada quando puder. Se fizer sentido, te explico como deixo no ar. Sem compromisso."
    )


def main():
    mestre = []
    for nicho in NICHOS:
        csvp = RAIZ / nicho / "_leads.csv"
        if not csvp.exists():
            print(f"  ! {csvp} nao existe (rode gerar.py antes)")
            continue
        leads = list(csv.DictReader(open(csvp, encoding="utf-8-sig"), delimiter=";"))

        md = [
            f"# Mensagens de primeiro contato - {nicho}",
            "",
            "Antes de enviar, se der, acrescente uma primeira linha pessoal: nome do dono,",
            "ou algo que você viu no Instagram deles. Isso dobra a taxa de resposta.",
            "",
            "Cadência de follow-up e condução do fechamento: ver o PDF de estratégia.",
            "",
            "---",
            "",
        ]
        for l in leads:
            empresa = l["nome"].strip()
            cidade = l["cidade"].strip()
            nota = (l["nota"] or "").strip()
            aval = (l["avaliacoes"] or "").strip()
            tem_nota = bool(nota) and nota not in ("0", "0,0")
            link = l["url"].strip()
            wa = "".join(ch for ch in l["whatsapp"] if ch.isdigit())
            msg = mensagem(empresa, cidade, nota if tem_nota else "", tem_nota, link, nicho)
            abrir = f"https://wa.me/{wa}?text={urllib.parse.quote(msg)}" if wa else ""

            md.append(f"## {empresa} ({cidade})")
            md.append("")
            md.append(f"- WhatsApp: `{wa}`  |  Prévia: {link}")
            if abrir:
                md.append(f"- Abrir conversa com a mensagem pronta: {abrir}")
            md.append("")
            md.append("```")
            md.append(msg)
            md.append("```")
            md.append("")

            mestre.append({
                "nicho": nicho,
                "empresa": empresa,
                "cidade": cidade,
                "whatsapp": wa,
                "link": link,
                "abrir": abrir,
                "mensagem": msg.replace("\n", " / "),
                "status": l.get("status", "") or "",
            })

        (RAIZ / nicho / "_MENSAGENS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"  {nicho:8s} {len(leads):4d} mensagens")

    with open(RAIZ / "_ENVIOS.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["nicho", "empresa", "cidade", "whatsapp", "link", "abrir", "mensagem", "status"],
            delimiter=";",
        )
        w.writeheader()
        w.writerows(mestre)
    print(f"\n  total: {len(mestre)}  ->  _ENVIOS.csv")


if __name__ == "__main__":
    main()
