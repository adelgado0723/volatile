<link src="{% static 'js/jquery.min.js' %}" > 
<script src="{% static 'js/jquery.min.js'%}"></script>

$(function () {
    "use strict";
    
    $(".popup img").click(function () {
        var $src = $(this).attr("src");
        $(".show").fadeIn();
        $(".img-show img").attr("src", $src);
    });
    
    $("span, .overlay").click(function () {
        $(".show").fadeOut();
    });
    
});
