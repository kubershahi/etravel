(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.tooltipped').tooltip();
    $('select').formSelect();


  }); // end of document ready
  
$(document).ready(function(){
	$('.materialboxed').materialbox();
 	$('select').formSelect();
  });
})(jQuery); // end of jQuery name space


document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);
  });