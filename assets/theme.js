/* Khul Ke Pucho — Aarogya theme JS. Deliberately tiny: t2/t3 data budgets. */
(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Quantity steppers on product + cart
  document.querySelectorAll('[data-qty-minus]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = btn.parentElement.querySelector('input[type=number]');
      var min = parseInt(input.min || '1', 10);
      input.value = Math.max(min, parseInt(input.value || '1', 10) - 1);
      input.dispatchEvent(new Event('change'));
    });
  });
  document.querySelectorAll('[data-qty-plus]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = btn.parentElement.querySelector('input[type=number]');
      input.value = parseInt(input.value || '1', 10) + 1;
      input.dispatchEvent(new Event('change'));
    });
  });
})();
