$(document).ready(function() {
  $('[data-toggle="toggle"]').change(function(){
    $(this).parents().next('.hide').toggle();
  });
});

function localize(t) {
  var d=new Date(t+" UTC").toLocaleTimeString('en-US',{ year:"numeric", month:"numeric", day:"numeric", second:"numeric", hour12: false, hour: '2-digit', minute: '2-digit', timeZoneName: "short" });;
  document.write(d.toString());
}