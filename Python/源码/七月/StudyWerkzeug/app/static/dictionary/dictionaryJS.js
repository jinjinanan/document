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


function backAndforth() {

    var o = $(".xm-carousel-list").css("margin-left");

    if(o == "0px")
    {
        $(".xm-carousel-list").css("margin-left","-1226px");
        // console.log(o);
    }
    else
    {
                $(".xm-carousel-list").css("margin-left","0px");


    }

        // console.log("阿" ,o);


};

$(document).ready(function () {
    setInterval(backAndforth,1000 *2);
});

function controlHomeSlider() {
    var mylist = $(".xm-slider").children();
    for(var i = 0 ;i < mylist.length; i++ )
    {
        var value = "float: none; position: absolute; display: block;";
        var value2 = "float: none; position: absolute;";
        var value1 = "float: none; position: absolute; display: none;";
        var a = mylist[i];
        var $a = $(a);



        // console.log($a.attr("style"),$a);
        if($a.attr("style") == value || $a.attr("style") == value2)
        {
            // $a.attr(;
            $a.fadeToggle();

            // $a.attr("style",value1);
            var $b =  $a.next();
            if(i < (mylist.length - 1))
            {

                $b.fadeToggle();
                // $b.attr("style",value)
            }
            else
            {

                $(mylist[0]).fadeToggle();
                // $(mylist[0]).attr("style",value)
            }

           break;
        }

    }
    console.log(mylist);

}

$(document).ready(function () {
    setInterval(controlHomeSlider,1000*3)
    // controlHomeSlider();

})