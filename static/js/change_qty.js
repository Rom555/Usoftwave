$(document).ready(function () {

  $(".cart-table__form").each(function(index) {
    const btn_minus = $(this).children(".cart-table__form-button_left");
    const btn_plus = $(this).children(".cart-table__form-button_right");
    const qty = $(this).children(".cart-table__input");
    
    btn_minus.click(function() {
      if (qty.val() > 1) {
        qty.val(qty.val() - 1)
      }
    })

    btn_plus.click(function() {
      if (qty.val() < 99) {
        qty.val(+qty.val() + 1)
      }
    })
  });
})