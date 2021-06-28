$(document).ready(function () {
  $(".newsletter__form").each(function () {
    $(this).validate({
      errorClass: "invalid",
      messages: {
        email: {
          required: "Email обязателен",
          email: "Email введен неправильно"
        },
      },
    });
  });

})