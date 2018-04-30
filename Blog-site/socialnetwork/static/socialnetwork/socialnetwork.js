var latest_post = "2018-01-01 00:01";
var latest_post_follow = "2018-01-01 00:01";
var latest_comment = "2018-01-01 00:01";

function getPosts() {

    if($("#page_mark").text()=="Global"){
        $.ajax({
            url: "/socialnetwork/get-posts-json",
            dataType : "json",
            data: "latest_post="+latest_post,
            success: updatePosts
        });

    }
    if($("#page_mark").text()=="Follow"){
        $.ajax({
            url: "/socialnetwork/get-posts-follow-json/"+$("#user_id").text(),
            dataType : "json",
            data: "latest_post_follow="+latest_post_follow,
            success: updatePosts
        });

    }
}


function getComments(){
    $.ajax({
        url: "/socialnetwork/get-comments-json",
        dataType : "json",
        data: "latest_comment="+latest_comment,
        success:  function(response) {
            if (Array.isArray(response)) {
                updateComments(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function updatePosts(posts) {

    // Remove old posts
    // $("li").remove();
    // Adds each post to the post area
     $(posts).each(function(){
        if(this.fields.post_time > latest_post_follow){
            $("#posts_area_follow").prepend(
                    '<li class="post">'+
                       '<p class="content">'+this.fields.post_content+'</p>'+
                       '<p class="whowhen"> By <a href="/socialnetwork/profile/'+this.fields.post_by_id+'">'+this.fields.post_by+' </a> <label id="when_follow">'+ this.fields.post_time+'</label></p>'+
                       '<div class="commentbox" id="commentbox'+this.pk+'">'+
                           '<div class="comment_add" >'+
                                '<input type="text"  id="new_comment'+this.pk+'" name="new_comment style="height:30px; width:600px">'+
                                '<button onclick="add_comment('+this.pk+')" style="height:30px;">Add comment</button>'+
                           "</div>"+
                       "</div><br>"+
                   "</li>"
            );
        }


        if(this.fields.post_time > latest_post){
            $("#posts_area").prepend(
                    '<li class="post">'+
                       '<p class="content">'+this.fields.post_content+'</p>'+
                       '<p class="whowhen"> By <a href="/socialnetwork/profile/'+this.fields.post_by_id+'">'+this.fields.post_by+' </a> <label id="when">'+ this.fields.post_time+'</label></p>'+
                       '<div class="commentbox" id="commentbox'+this.pk+'">'+
                           '<div class="comment_add" >'+
                                '<input type="text"  id="new_comment'+this.pk+'" name="new_comment style="height:30px; width:600px">'+
                                '<button onclick="add_comment('+this.pk+')" style="height:30px;">Add comment</button>'+
                           "</div>"+
                       "</div><br>"+
                   "</li>"
            );
        }


        });

      getComments();
     if($("#when:first").text() != "")
        latest_post = $("#when:first").text();
     if($("#when_follow:first").text() != "")
        latest_post_follow = $("#when_follow:first").text();
}

function updateComments(comments) {
    // Remove old comments
    temp = latest_comment;
    //Add new comments
    $(comments).each(function(){


        if(this.fields.comment_time > latest_comment){

            if(this.fields.comment_time > temp)
                temp = this.fields.comment_time;
            var post_num = this.fields.post_id;
            $("#commentbox"+post_num).append(
                '<p class="comment" id="comment">'+ this.fields.comment_content+' --Comment by <a href="/socialnetwork/profile/'+this.fields.comment_by_id+'">'+
                this.fields.comment_by+' </a> '+this.fields.comment_time+'</p>'

            );
        }

    });
    latest_comment = temp;
}


function add_comment(post_id) {
    var commentTextElement = $("#new_comment"+post_id);
    var commentTextValue   = commentTextElement.val();
    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment/"+post_id,
        type: "POST",
        data: "new_comment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                getComments();
            } else {
                displayError(response.error);
            }
        }
    });
}



function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}


function displayError(message) {
    $("#error").html(message);
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}




// Call getPosts as soon as page is finished loading
window.onload = getPosts;

// causes Posts to be re-fetched every 5 seconds
window.setInterval(getPosts, 5000);
