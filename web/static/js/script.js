const activePage = window.location.pathname;
const navLinks = document.querySelectorAll("nav a").forEach((link) => {
  if (link.href.includes(`${activePage}`)) {
    link.classList.add("active");
  }
});

if (
  window.location.pathname.includes("/view-product") ||
  window.location.pathname.includes("/profile") ||
  window.location.pathname.includes("/edit-personal-info") ||
  window.location.pathname.includes("/search") ||
  window.location.pathname.includes("brands")
) {
  const nav = document.querySelector(".nav");
  const menu_btn = document.querySelectorAll(".menu-btn");
  const search_box = document.querySelector(".search-box");
  const btn_container = document.querySelector(".back-btn-container");
  const menu_dismis_btn = document.querySelector(".menu-dismis-btn");
  const header_logo = document.querySelector(".header-logo");

  nav.style.display = "none";
  menu_btn.forEach((btn) => {
    btn.style.display = "none";
  });
  search_box.style.display = "none";
  menu_dismis_btn.style.display = "block";
  header_logo.children[0].style.display = "none";
  header_logo.children[1].style.display = "none";
  header_logo.children[2].style.display = "none";
  header_logo.children[3].style.display = "flex";

  btn_container.innerHTML = `<button class="back-btn" style="font-size: 1rem; background: none; border: none; font-weight: 800; width: 20px;"><i class="fas fa-arrow-left"></i></button>`;

  btn_container.style.display = "block";
  btn_container.addEventListener("click", (event) => {
    window.location.href = "/";
  });
}

if (
  window.location.pathname.includes("/products") ||
  window.location.pathname.includes("/search") ||
  window.location.pathname.includes("flash-sale") ||
  window.location.pathname.includes("brands")
) {
  const filterEl = document.getElementById("filter");
  const mobile_filter = document.getElementById("mobile-filter");
  const productCat = document.querySelectorAll(".p-category");

  filterEl.style.display = "block";

  filterEl.addEventListener("input", (event) => {
    productCat.forEach((cat) => {
      let searchQuery = cat.textContent.toLowerCase();
      let searchData = filterEl.value.toLowerCase();

      if (searchData == "all") {
        cat.parentNode.parentNode.classList.remove("hide");
      } else {
        cat.parentNode.parentNode.classList.toggle(
          "hide",
          searchQuery != searchData,
        );
      }
    });
  });

  mobile_filter.addEventListener("input", (event) => {
    productCat.forEach((cat) => {
      let searchQuery = cat.textContent.toLowerCase();
      let searchData = mobile_filter.value.toLowerCase();

      if (searchData == "all") {
        cat.parentNode.parentNode.classList.remove("hide");
      } else {
        cat.parentNode.parentNode.classList.toggle(
          "hide",
          searchQuery != searchData,
        );
      }
    });
  });
}

if (window.location.pathname.includes("brands")) {
  const filterEl = document.getElementById("filter");
  const mobile_filter = document.getElementById("mobile-filter");
  const productCat = document.querySelectorAll(".p-category");

  filterEl.style.display = "block";
  mobile_filter.style.display = "block";

  filterEl.addEventListener("input", (event) => {
    productCat.forEach((cat) => {
      let searchQuery = cat.textContent.toLowerCase();
      let searchData = filterEl.value.toLowerCase();

      if (searchData == "all") {
        cat.parentNode.parentNode.classList.remove("hide");
      } else {
        cat.parentNode.parentNode.classList.toggle(
          "hide",
          searchQuery != searchData,
        );
      }
    });
  });

  mobile_filter.addEventListener("input", (event) => {
    productCat.forEach((cat) => {
      let searchQuery = cat.textContent.toLowerCase();
      let searchData = mobile_filter.value.toLowerCase();

      if (searchData == "all") {
        cat.parentNode.parentNode.classList.remove("hide");
      } else {
        cat.parentNode.parentNode.classList.toggle(
          "hide",
          searchQuery != searchData,
        );
      }
    });
  });
}

if (
  window.location.pathname === "/" ||
  window.location.pathname.includes("/products") ||
  window.location.pathname.includes("/search")
) {
  const searchEl = document.getElementById("search-box");
  searchEl.style.display = "flex";
}

if (
  window.location.pathname.includes("/profile") ||
  window.location.pathname.includes("/edit-personal-info")
) {
  const profile = document.querySelectorAll(".header-logo button");
  profile.forEach((btn) => {
    btn.style.display = "none";
  });
}

function change_image(img_src) {
  const main_image = document.querySelector(".main-img");
  const img_btn = document.querySelectorAll(".nav-image-box button");

  main_image.setAttribute("src", `.${img_src}`);

  img_btn.forEach((btn) => {
    if (
      main_image.getAttribute("src") !== btn.children[0].getAttribute("src")
    ) {
      btn.classList.remove("image-active");
      btn.children[1].style.display = "none";
    } else {
      btn.classList.toggle("image-active", true);
      btn.children[1].style.display = "block";
    }
  });
}

const add_to_cart = document
  .querySelectorAll(".add-to-cart-btn")
  .forEach((btn) => {
    btn.addEventListener("click", (event) => {
      var id = btn.getAttribute("pid").toString();
      var cart_quantity = document.querySelectorAll("#cart-count");

      fetch("/add-to-cart")
        .then((response) => response.json())
        .then((json) => {
          cart_quantity.forEach((qt) => {
            qt.textContent = json.new_cart_quantity;
          });
          btn.textContent = json.flash_message;
          btn.style.background = "linear-gradient(135deg, green, lightgreen)";
          setTimeout(function () {
            btn.textContent = "Add to cart";
            btn.style.background = "linear-gradient(135deg, #6366f1, #06b6d4)";
          }, 3000);
        });

      fetch("/add-to-cart", {
        method: "POST",
        body: JSON.stringify({ product_id: id }),
      });
    });
  });

const plus_cart_btn = document
  .querySelectorAll(".plus-cart-btn")
  .forEach((btn) => {
    btn.addEventListener("click", (event) => {
      var id = btn.getAttribute("pid").toString();
      var quantity = btn.parentNode.children[1];
      var item_total = btn.parentNode.parentNode.children[3];
      var subtotal = document.querySelector(".subtotal");
      var cart_total = document.querySelector(".cart-total");

      fetch("/plus-cart")
        .then((response) => response.json())
        .then((json) => {
          quantity.textContent = json.quantity;
          item_total.textContent = "$" + json.item_total + ".0";
          subtotal.textContent = "$" + json.amount + ".0";
          cart_total.textContent = "$" + json.total + ".0";
        });

      fetch("/plus-cart", {
        method: "POST",
        body: JSON.stringify({ cart_id: id }),
      });
    });
  });

const minus_cart_btn = document
  .querySelectorAll(".minus-cart-btn")
  .forEach((btn) => {
    btn.addEventListener("click", (event) => {
      var id = btn.getAttribute("pid").toString();
      var quantity = btn.parentNode.children[1];
      var item_total = btn.parentNode.parentNode.children[3];
      var subtotal = document.querySelector(".subtotal");
      var cart_total = document.querySelector(".cart-total");

      fetch("/minus-cart")
        .then((response) => response.json())
        .then((json) => {
          quantity.textContent = json.quantity;
          item_total.textContent = "$" + json.item_total + ".0";
          subtotal.textContent = "$" + json.amount + ".0";
          cart_total.textContent = "$" + json.total + ".0";
        });

      fetch("/minus-cart", {
        method: "POST",
        body: JSON.stringify({ cart_id: id }),
      });
    });
  });

const remove_cart_btn = document
  .querySelectorAll(".remove-cart-btn")
  .forEach((btn) => {
    btn.addEventListener("click", (event) => {
      var id = btn.getAttribute("pid").toString();
      var item_to_remove = btn.parentNode;

      fetch("/remove-cart")
        .then((response) => response.json())
        .then((json) => {
          subtotal.textContent = "$" + json.amount + ".0";
          cart_total.textContent = "$" + json.total + ".0";
          item_to_remove.remove();
        });

      fetch("/remove-cart", {
        method: "POST",
        body: JSON.stringify({ cart_id: id }),
      }).then((_res) => {
        window.location.href = "/cart";
      });
    });
  });

const showDropDownBtn = document.querySelector(".btn-show-dropdown");
const hideDropDownBtn = document.querySelector(".btn-hide-dropdown");
const dropDownMenu = document.querySelector(".dropdown-menu");

showDropDownBtn.addEventListener("click", (event) => {
  showDropDownBtn.style.display = "none";
  hideDropDownBtn.style.display = "block";
  dropDownMenu.style.transform = "translateY(0)";
  dropDownMenu.style.transition = ".5s";
});

hideDropDownBtn.addEventListener("click", (event) => {
  hideDropDownBtn.style.display = "none";
  showDropDownBtn.style.display = "block";
  dropDownMenu.style.transform = "translateY(-120%)";
  dropDownMenu.style.transition = ".5s";
});

if (
  window.location.pathname.includes("edit-personal-info") ||
  window.location.pathname.includes("personal-info")
) {
  const region = document.getElementById("region");
  const town = document.getElementById("town");

  region.addEventListener("input", changeTown);

  function changeTown() {
    if (region.value == "greater accra region") {
      town.innerHTML = '<option value="accra">Accra</option>';
    }
    if (region.value == "ashanti region") {
      town.innerHTML = '<option value="kumasi">Kumasi</option>';
    }
    if (region.value == "central region") {
      town.innerHTML = '<option value="cape coast">Cape Coast</option>';
    }
    if (region.value == "western region") {
      town.innerHTML =
        '<option value="secondi-takoradi">Secondi-Takoradi</option>';
    }
    if (region.value == "eastern region") {
      town.innerHTML = '<option value="koforidua">Koforidua</option>';
    }
    if (region.value == "volta region") {
      town.innerHTML = '<option value="ho">Ho</option>';
    }
    if (region.value == "northern region") {
      town.innerHTML = '<option value="tamale">Tamale</option>';
    }
    if (region.value == "upper east region") {
      town.innerHTML = '<option value="bolgatanga">Bolgatanga</option>';
    }
    if (region.value == "upper west region") {
      town.innerHTML = '<option value="wa">Wa</option>';
    }
    if (region.value == "bono region") {
      town.innerHTML = '<option value="sunyani">Sunyani</option>';
    }
    if (region.value == "bono east region") {
      town.innerHTML = '<option value="techiman">Techiman</option>';
    }
    if (region.value == "ahafo region") {
      town.innerHTML = '<option value="goaso">Goaso</option>';
    }
    if (region.value == "savannah region") {
      town.innerHTML = '<option value="damongo">Damongo</option>';
    }
    if (region.value == "north east region") {
      town.innerHTML = '<option value="nalerigu">Nalerigu</option>';
    }
    if (region.value == "western north region") {
      town.innerHTML = '<option value="sefwi wiawso">Sefwi Wiawso</option>';
    }
    if (region.value == "oti region") {
      town.innerHTML = '<option value="dambai">Dambai</option>';
    }
  }
}

function navBarToggleOpen() {
  const sideBar = document.getElementById("sidebar");
  sideBar.style.display = "flex";
  sideBar.style.transform = "translateX(0%)";
  sideBar.style.zIndex = "2000";
  sideBar.style.transition = "0.3s";
}
function navBarToggleClose() {
  const sideBar = document.getElementById("sidebar");
  sideBar.style.display = "flex";
  sideBar.style.transform = "translateX(-100%)";
  sideBar.style.transition = "0.3s";
}

const view_btns = document.querySelectorAll(".btn-view-brand");

view_btns.forEach((btn) => {
  let id = btn.getAttribute("pid");

  btn.addEventListener("click", (event) => {
     console.log(id)
     window.location.href = `/view-product/${id}`
  });
});
