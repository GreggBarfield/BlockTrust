/*

Template: Technol - Responsive Website Template
Author: potenzaglobalsolutions
Design and Developed by: potenzaglobalsolutions.com

NOTE: This file contains all scripts for the actual Template.

*/

/*================================================
[  Table of contents  ]
================================================


======================================
[ End table content ]
======================================*/


  if ($(".section-navbar").length != 0) {

      // jQuery Smooth Scroll
      $('.page-scroll').on('click', function(event) {
          var $anchor = $(this),
              headerH = '100';
          $('html , body').stop().animate({
              scrollTop: $($anchor.attr('href')).offset().top - headerH + "px",
          }, 1200, 'easeInOutExpo');

          event.preventDefault();
      });
  }

  $('.section-navbar li').on('click', function(){
      $(this).addClass('active').siblings().removeClass('active');
  });




  $('[data-toggle="tooltip"]').tooltip()
