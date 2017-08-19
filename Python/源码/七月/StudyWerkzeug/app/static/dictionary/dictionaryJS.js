/**
 * Created by chenlinbo on 14/08/2017.
 */
$(document).ready(function () {
    $(".brick-item").mouseover(function () {
        $(this).attr({class:"brick-item-m brick-item brick-item-active"});
    });
    $(".brick-item").mouseout(function () {
        $(this).attr({class:"brick-item-m brick-item"});
    })
});

$(document).ready(function(){
  $(".title").click(function(){
    $(this).hide();
  });
});


