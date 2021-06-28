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
        confirm_password: {
          required: "Подтвердите пароль",
          minlength: "Пароль слишком короткий",
        },
        first_name: {
          required: "Имя обязательно",
          minlength: "Имя слишком короткое",
        },
        last_name: {
          required: "Фамилия обязательна",
          minlength: "Фамилия слишком короткая",
        },
        phone: {
          required: "Телефон обязателен",
          minlength: "Введите телефон полностью",
          maxlength: "Слишком много символов",
        },
        email: {
          required: "Email обязателен",
          email: "Ваш email должен быть в формате name@domain.com",
        },
      },
    });
  });

  $("[type=tel]").each(function () {
    $(this).mask("+7 (000) 000-00-00");
  });
})