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

// Contagem regressiva da promoção, iniciada quando a página é carregada.
(function showPromoTimer() {
  const timers = document.querySelectorAll("[data-promo-timer]");
  if (!timers.length) return;

  const endTime = Date.now() + 5 * 60 * 1000;
  const update = () => {
    const remaining = Math.max(0, endTime - Date.now());
    const totalSeconds = Math.ceil(remaining / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    timers.forEach((timer) => {
      const time = timer.querySelector("[data-promo-time]");
      if (remaining > 0) {
        time.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
      } else {
        timer.textContent = "O prazo da promoção terminou.";
      }
      timer.hidden = false;
    });

    if (remaining === 0) clearInterval(interval);
  };

  const interval = setInterval(update, 1000);
  update();
})();

// Esconde a barra fixa de compra enquanto outro botão de compra estiver na tela.
(function toggleStickyBar() {
  const sticky = document.querySelector(".sticky");
  const buttons = document.querySelectorAll("main .buy");
  if (!sticky || !("IntersectionObserver" in window)) return;

  const visible = new Set();
  sticky.classList.add("is-hidden");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) visible.add(entry.target);
      else visible.delete(entry.target);
    });
    sticky.classList.toggle("is-hidden", visible.size > 0);
  }, { rootMargin: "0px 0px -80px 0px" });

  buttons.forEach((button) => observer.observe(button));
})();

// Envia cada clique de compra para a propriedade do Google Analytics do botão.
document.querySelectorAll("[data-ga-id]").forEach((button) => {
  button.addEventListener("click", () => {
    gtag("event", button.dataset.gaEvent, { send_to: button.dataset.gaId, transport_type: "beacon" });
  });
});

document.getElementById("year").textContent = new Date().getFullYear();
