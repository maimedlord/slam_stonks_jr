$(document).ready(function() {
  $('a').click(function(event) {
    var id = $(this).attr("id");

    if (id == 'lnkmngclients') {
      $('#clientdiv').hide();
      $('#memebersdiv').show();
    }
    if (id == 'lnkclientdiv') {
      $('#clientdiv').show();
      $('#memebersdiv').hide();
    }
  });
});