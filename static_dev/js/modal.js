$(document).ready(function () {
  //Модальное окно бургер
  $(".header-button").on("click", function () {
    $(".header-links").removeClass("header-links_visible");
  });
  $(".menu-button").on("click", function () {
    $(".header-links").addClass("header-links_visible");
  });

  //Модальное окно логин
  $(".header__login").on("click", function () {
    $(".header-login").slideToggle(300);
  })
})