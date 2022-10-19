$(document).ready(function() {
 $(document).on('click', '.checkbox', function() {
    console.log("11111");
 $(this).parent().addClass('completed');
 ///$(this).attr('disabled', true);

 uid = $(this).attr('data-uid');

 document.location.href = "complete/"+ uid;

}) 

}) 
