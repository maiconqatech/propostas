// Varal de luzes do topo (decorativo).
(function drawGarland() {
  const svg = document.getElementById("garland");
  const SEGMENT = 120;
  const COLORS = ["#f2b632", "#e5534b", "#7fd1a8"];
  const POINTS = [[30, 28], [60, 33], [90, 28]];
  let wire = "M0 6";
  let bulbs = "";

  for (let segment = 0; segment < 12; segment++) {
    wire += ` Q${segment * SEGMENT + 60} 46 ${(segment + 1) * SEGMENT} 6`;
    POINTS.forEach(([x, y], index) => {
      const color = COLORS[(segment + index) % COLORS.length];
      const delay = (segment * 3 + index) * 170;
      bulbs += `<circle class="bulb" cx="${segment * SEGMENT + x}" cy="${y}" r="5" fill="${color}" style="animation-delay:${delay}ms"/>`;
    });
  }

  svg.innerHTML = `<path d="${wire}" fill="none" stroke="#f8f1e3" stroke-opacity=".35" stroke-width="1.5"/>${bulbs}`;
})();

// Contagem real até o próximo Natal, no horário de Brasília. Só aparece na temporada.
(function showCountdown() {
  const today = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date());
  const year = Number(today.slice(0, 4));
  const christmas = `${year}-12-25`;
  const target = today > christmas ? `${year + 1}-12-25` : christmas;
  const days = Math.round((Date.parse(target) - Date.parse(today)) / 86400000);

  if (days <= 0 || days > 90) return;

  const text = days === 1 ? "Falta 1 dia para o Natal" : `Faltam ${days} dias para o Natal`;
  document.querySelectorAll("[data-countdown]").forEach((element) => {
    element.textContent = text;
    element.hidden = false;
  });
})();

document.getElementById("year").textContent = new Date().getFullYear();
