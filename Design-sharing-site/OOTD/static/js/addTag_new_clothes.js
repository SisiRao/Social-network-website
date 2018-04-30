$(document).ready(function() {

        $("#imageMap").click(function(e){

            var image_left = $(this).offset().left;
            var click_left = e.pageX;
            var left_distance = click_left - image_left;

            var image_top = $(this).offset().top;
            var click_top = e.pageY;
            var top_distance = click_top - image_top;

            var mapper_width = $('#mapper').width();
            var imagemap_width = $('#imageMap').width();

            var mapper_height = $('#mapper').height();
            var imagemap_height = $('#imageMap').height();

            if((top_distance + mapper_height > imagemap_height) && (left_distance + mapper_width > imagemap_width)){
                $('#mapper .tagged_circle').css("display","block");
                $('#mapper').css("left", (click_left - mapper_width - image_left  ))
                .css("top",(click_top - mapper_height - image_top  ))
                .css("width","50px")
                .css("height","50px")
                .show();

                $('#tag-top').val((click_top - mapper_height - image_top)/imagemap_height);
                $('#tag-left').val((click_left - mapper_width - image_left)/imagemap_width);

            }
            else if(left_distance + mapper_width > imagemap_width){

                $('#mapper .tagged_circle').css("display","block");
                $('#mapper').css("left", (click_left - mapper_width - image_left  ))
                .css("top",top_distance)
                .css("width","50px")
                .css("height","50px")
                .show();

                $('#tag-top').val(top_distance/imagemap_height);
                $('#tag-left').val((click_left - mapper_width - image_left  )/imagemap_width);
    
            }
            else if(top_distance + mapper_height > imagemap_height){

                $('#mapper .tagged_circle').css("display","block");
                $('#mapper').css("left", left_distance)
                .css("top",(click_top - mapper_height - image_top  ))
                .css("width","50px")
                .css("height","50px")
                .show();

                $('#tag-top').val((click_top - mapper_height - image_top  )/imagemap_height);
                $('#tag-left').val(left_distance/imagemap_width);
            }
            else{
                $('#mapper .tagged_circle').css("display","block");
                $('#mapper').css("left",left_distance)
                .css("top",top_distance)
                .css("width","50px")
                .css("height","50px")
                .show();

                $('#tag-top').val(top_distance/imagemap_height);
                $('#tag-left').val(left_distance/imagemap_width);
            }

            $("#mapper").draggable({ containment: "parent" });


            
        });


        $("#mapper").mouseup(function(e){

            var image_left = $("#imageMap").offset().left;
            var click_left = e.pageX;
            var left_distance = click_left - image_left;

            var image_top = $("#imageMap").offset().top;
            var click_top = e.pageY;
            var top_distance = click_top - image_top;

            var mapper_width = $(this).width();
            var imagemap_width = $('#imageMap').width();

            var mapper_height = $(this).height();
            var imagemap_height = $('#imageMap').height();

            if((top_distance + mapper_height > imagemap_height) && (left_distance + mapper_width > imagemap_width)){

                $('#tag-top').val((click_top - mapper_height - image_top)/imagemap_height);
                $('#tag-left').val((click_left - mapper_width - image_left)/imagemap_width);

            }
            else if(left_distance + mapper_width > imagemap_width){

                $('#tag-top').val(top_distance/imagemap_height);
                $('#tag-left').val((click_left - mapper_width - image_left  )/imagemap_width);
    
            }
            else if(top_distance + mapper_height > imagemap_height){
                $('#tag-top').val((click_top - mapper_height - image_top  )/imagemap_height);
                $('#tag-left').val(left_distance/imagemap_width);
            }
            else{

                $('#tag-top').val(top_distance/imagemap_height);
                $('#tag-left').val(left_distance/imagemap_width);
            }
            
        });

    });