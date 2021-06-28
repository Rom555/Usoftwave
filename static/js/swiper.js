$(document).ready(function () {
  var saleSwiper = new Swiper(".sale-slider", {
    loop: true,
    spaceBetween: 60,
    centeredSlides: true,
    navigation: {
      nextEl: ".sale-slider__button--next",
      prevEl: ".sale-slider__button--prev",
    },
  })

  var commentsSwiper = new Swiper(".comments__swiper-container", {
    loop: true,
    spaceBetween: 60,
    centeredSlides: true,
    pagination: {
      el: ".comments__swiper-pagination",
      renderBullet: function (index, className) {
        return '<span class="' + className + '"></span>';
      },
      bulletClass: "comments__swiper-pagination-bullet",
      bulletActiveClass: "comments__swiper-pagination-bullet-active",
      clickable: true,
    },
    autoplay: {
      delay: 7000,
      disableOnInteraction: false,
    },
  });

  var commentsSwiperSlide = $(".comments__swiper-container");
  commentsSwiperSlide.on("mouseover", function () {
    commentsSwiper.autoplay.stop();
  });
  commentsSwiperSlide.on("mouseout", function () {
    commentsSwiper.autoplay.start();
  });
})