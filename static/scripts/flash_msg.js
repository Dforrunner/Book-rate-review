// If message is success message, then auto close msg
$(document).ready(function(){
    $(".alert-success").delay(5000).slideUp(300);
});

// Close message when close (x) button is clicked
$(document).ready(function() {
  $(".close-flash-btn").click(function() {
    $(".message-flash").slideUp("slow");
  });
});
