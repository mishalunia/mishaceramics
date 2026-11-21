(function () {
  function masonryLayout() {
    var wrap = document.querySelector(".masonry");
    if (!wrap) return;
    var items = [].slice.call(wrap.querySelectorAll(".asset"));
    if (!items.length) return;
    var cols = 3;
    if (window.innerWidth <= 767) cols = 1;
    else if (window.innerWidth <= 1100) cols = 2;
    items.forEach(function (item) {
      item.style.position = "";
      item.style.left = "";
      item.style.top = "";
      item.style.width = "";
    });
    wrap.style.height = "";
    if (cols === 1) return;
    var heights = [];
    var i;
    for (i = 0; i < cols; i++) heights[i] = 0;
    var colW = wrap.clientWidth / cols;
    items.forEach(function (item) {
      item.style.position = "absolute";
      item.style.width = 100 / cols + "%";
      var col = heights.indexOf(Math.min.apply(null, heights));
      item.style.left = col * colW + "px";
      item.style.top = heights[col] + "px";
      heights[col] += item.offsetHeight;
    });
    wrap.style.height = Math.max.apply(null, heights) + "px";
  }

  function whenImagesReady(cb) {
    var imgs = document.querySelectorAll(".masonry img");
    var left = imgs.length;
    if (!left) {
      cb();
      return;
    }
    function done() {
      left -= 1;
      if (left <= 0) cb();
    }
    imgs.forEach(function (img) {
      if (img.complete) done();
      else {
        img.addEventListener("load", done);
        img.addEventListener("error", done);
      }
    });
  }

  whenImagesReady(masonryLayout);
  window.addEventListener("resize", masonryLayout);

  var burger = document.querySelector(".hamburger");
  if (burger) {
    burger.addEventListener("click", function () {
      document.body.classList.toggle("menu-open");
    });
  }

  var cartDrawer = document.querySelector(".cart-drawer-wrap");
  if (!cartDrawer) {
    cartDrawer = document.createElement("div");
    cartDrawer.className = "cart-drawer-wrap";
    cartDrawer.innerHTML =
      '<div class="cart-backdrop" tabindex="-1"></div>' +
      '<aside class="cart-drawer" role="dialog" aria-modal="true" aria-labelledby="cart-title">' +
        '<div class="cart-drawer-head">' +
          '<h2 id="cart-title">Cart</h2>' +
          '<button type="button" class="cart-close" aria-label="Close cart"></button>' +
        "</div>" +
        '<p class="cart-empty">Your cart is empty.</p>' +
      "</aside>";
    document.body.appendChild(cartDrawer);
  }

  function openCart() {
    document.body.classList.add("cart-open");
    var closeBtn = cartDrawer.querySelector(".cart-close");
    if (closeBtn) closeBtn.focus();
  }

  function closeCart() {
    document.body.classList.remove("cart-open");
  }

  document.querySelectorAll(".cart-btn").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      openCart();
    });
  });

  cartDrawer.querySelector(".cart-backdrop").addEventListener("click", closeCart);
  cartDrawer.querySelector(".cart-close").addEventListener("click", closeCart);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.body.classList.contains("cart-open")) closeCart();
  });

  document.querySelectorAll(".add-cart").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      toast("currently out of stock");
    });
  });

  function toast(msg) {
    var t = document.querySelector(".toast");
    if (!t) {
      t = document.createElement("div");
      t.className = "toast";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(function () { t.classList.remove("show"); }, 2500);
  }
})();
