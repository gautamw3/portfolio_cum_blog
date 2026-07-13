/************************************
* Configure toaster js notification *
*************************************/
$(document).ready(function() {
	toastr.options = {
	  "closeButton": true,
	  "debug": false,
	  "newestOnTop": true,
	  "progressBar": true,
	  "positionClass": "toast-bottom-right",
	  "preventDuplicates": true,
	  "onclick": null,
	  "showDuration": "300",
	  "hideDuration": "1000",
	  "timeOut": "5000",
	  "extendedTimeOut": "1000",
	  "showEasing": "swing",
	  "hideEasing": "linear",
	  "showMethod": "fadeIn",
	  "hideMethod": "fadeOut"
	}

  <!-- Menu Toggle Script -->
  if($("#menu-toggle").length) {
    $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#wrapper").toggleClass("toggled");
    });
  }

    if ($("#success").length != 0) {
        toastr['success']('Query form submitted successfully', 'Thanks & wait for our response');
        $("#id_client_name, #id_client_email, #id_subject, #id_file_supporting_the_message, #id_message").val('');
    }
    if ($("#error").length != 0) {
        toastr['error']('There are some exceptions within the form input', 'Please fix the errors displayed');
    }

    // Init MixItUp
    if($('#mix-container').length == 1) {
      const containerEl = document.querySelector('#mix-container');
      const mixer = mixitup(containerEl, {
        selectors: {
          target: '.mix'
        },
        animation: {
          duration: 300
        }
      });
    }

	  // Active class toggle for filter buttons
	  const filterButtons = document.querySelectorAll('.portfolio-filter-btn');
	  filterButtons.forEach(btn => {
		btn.addEventListener('click', function() {
		  filterButtons.forEach(b => b.classList.remove('active'));
		  this.classList.add('active');
		});
	  });

    if($(".glide__slide").length > 0) {
        const glideElement = document.querySelector('.glide');
        if (glideElement) {
            const glide = new Glide(glideElement, {
                type: 'carousel',
                startAt: 0,
                perView: 1,
                gap: 30,
                autoplay: 5000,
                hoverpause: true,
                animationDuration: 800,
                animationTimingFunc: 'ease-in-out'
              });

              glide.on(['mount.after', 'run.after'], () => {
                document.querySelectorAll('.testimonial-card').forEach(card => {
                  card.classList.remove('active');
                });

                const activeSlide = document.querySelector('.glide__slide--active .testimonial-card');
                if (activeSlide) {
                  setTimeout(() => activeSlide.classList.add('active'), 50);
                }
              });
            glide.mount();
        }
    }

      if (document.querySelector('.new-banner-slider')) {
        const swiper = new Swiper('.new-banner-slider', {
          loop: true,
          autoplay: {
            delay: 5000,
            disableOnInteraction: false,
          },
          effect: 'fade',
          pagination: {
            el: '.swiper-pagination',
            clickable: true,
          },
          navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
          },
        });
      }

      const header = document.querySelector('.custom-header');
      if (header) {
        const updateHeaderState = function () {
          header.classList.toggle('is-scrolled', window.scrollY > 24);
        };
        updateHeaderState();
        document.addEventListener('scroll', updateHeaderState);
      }
});