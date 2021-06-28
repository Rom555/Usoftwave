$(document).ready(function () {
  $(".forms__form").each(function () {
    $(this).validate({
      errorClass: "invalid",
      messages: {
        username: {
          required: "Логин обязателен",
          minlength: "Логин слишком короткий",
        },
        password: {
          required: "Пароль обязателен",
          minlength: "Пароль слишком короткий",
        },
      },
    });
  });

})