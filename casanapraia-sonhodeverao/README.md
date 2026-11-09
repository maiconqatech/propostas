# Sonho de Verão — landing page da casa em Peruíbe

Landing page de divulgação da casa **Sonho de Verão**, disponível para
aluguel de temporada em Peruíbe/SP. Reúne fotos, comodidades, localização
e avaliações extraídas do anúncio no Airbnb, com foco em levar o visitante
a reservar direto pelo WhatsApp do anfitrião.

## Stack

Página estática, sem build nem dependências:

- `index.html` — HTML + CSS puro (vanilla), sem frameworks
- `images/` — fotos reais do imóvel
- Botão flutuante e CTAs de WhatsApp (`wa.me`) com mensagem pré-preenchida
- Bloco de localização com endereço e link direto para o Google Maps

## Rodando localmente

```bash
# Windows
start index.html
```

## Deploy

HTML estático, publica em qualquer hospedagem sem configuração:

- **GitHub Pages**: deploy automático via GitHub Actions a cada push em `main`
- **Vercel / Netlify**: importe o repositório, sem build command

## Publicado em

https://maiconqatech.github.io/sonho-de-verao/
