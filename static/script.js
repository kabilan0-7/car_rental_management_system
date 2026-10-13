document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menuToggle");
  const nav = document.getElementById("mainNav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const opened = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(opened));
    });
  }

  const search = document.getElementById("carSearch");
  const category = document.getElementById("categoryFilter");
  const cards = Array.from(document.querySelectorAll(".searchable-car"));
  const count = document.getElementById("carCount");
  const empty = document.getElementById("emptyCars");
  function filterCars() {
    if (!cards.length) return;
    const query = (search?.value || "").toLowerCase().trim();
    const selected = category?.value || "";
    let visible = 0;
    cards.forEach(card => {
      const matches = card.dataset.name.includes(query) && (!selected || card.dataset.category === selected);
      card.hidden = !matches;
      if (matches) visible++;
    });
    if (count) count.textContent = `${visible} car${visible === 1 ? "" : "s"}`;
    if (empty) empty.hidden = visible !== 0;
  }
  search?.addEventListener("input", filterCars);
  category?.addEventListener("change", filterCars);

  const form = document.getElementById("bookingForm");
  if (form) {
    const carSelect = document.getElementById("carSelect");
    const pickup = document.getElementById("pickupDate");
    const ret = document.getElementById("returnDate");
    const rate = document.getElementById("dailyRate");
    const daysText = document.getElementById("rentalDays");
    const totalText = document.getElementById("estimateTotal");
    const money = n => "₹" + Math.round(n).toLocaleString("en-IN");

    function estimate() {
      const option = carSelect?.selectedOptions[0];
      const price = Number(option?.dataset.price || 0);
      if (rate) rate.textContent = price ? money(price) : "Choose a car";
      if (pickup && ret && pickup.value) {
        ret.min = pickup.value;
      }
      const start = pickup?.value ? new Date(pickup.value + "T00:00:00") : null;
      const end = ret?.value ? new Date(ret.value + "T00:00:00") : null;
      const days = start && end ? Math.ceil((end - start) / 86400000) : 0;
      if (daysText) daysText.textContent = days > 0 ? `${days} day${days === 1 ? "" : "s"}` : "Select dates";
      const extras = Array.from(form.querySelectorAll('input[name="extras"]:checked')).reduce((sum, el) => sum + (el.value === "child-seat" ? 500 : el.value === "wifi" ? 300 : 0), 0);
      if (totalText) totalText.textContent = price && days > 0 ? money(price * days + extras) : "—";
    }
    [carSelect, pickup, ret, ...form.querySelectorAll('input[name="extras"]')].forEach(el => el?.addEventListener("change", estimate));
    form.addEventListener("submit", event => {
      if (pickup?.value && ret?.value && ret.value <= pickup.value) {
        event.preventDefault();
        ret.setCustomValidity("Return date must be after the pickup date.");
        ret.reportValidity();
      } else if (ret) {
        ret.setCustomValidity("");
      }
    });
    ret?.addEventListener("input", () => ret.setCustomValidity(""));
    estimate();
  }
});
