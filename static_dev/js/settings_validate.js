$(document).ready(function () {
  $(".forms__form").each(function () {
    $(this).validate({
      errorClass: "invalid",
      messages: {
        old_password: {
          required: "Старый пароль обязателен",
          minlength: "Пароль слишком короткий",
        },
        new_password1: {
          required: "Новый пароль обязателен",
          minlength: "Пароль слишком короткий",
        },
        new_password2: {
          required: "Подтвердите пароль",
          minlength: "Пароль слишком короткий",
        }
      },
    });
  });
})