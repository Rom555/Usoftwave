$(document).ready(function () {
  $(".modal__button").click(function() {
      dataAttr = $(this).data("target")
      $(dataAttr).addClass("modal-open")
  })

  $(".modal__close").click(function() {
    $(".modal").removeClass("modal-open");
  })
})