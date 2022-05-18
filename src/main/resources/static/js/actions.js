function toggle() {
  if( $("#vegetarian").is(':checked')) {
    $(".meatSelection").hide();
  } else {
    $(".meatSelection").show();
  }
}