var max_pk = 0;
var prev_pk = 0;
var pk_len = 0;

function getInitPK(){
    // console.log(max_date);
    $.ajax({
        url: "/OOTD/get-list-json/"+max_pk,
        dataType: "json",
        success : updateInitPK
    });

}

function updateInitPK(posts){
    if($(posts).length) {
        pk_len = $(".item").length;
        max_pk = posts[posts.length - 1].pk;
        $("#new-msg-container").empty().append(
			"<a id=\"new-msg-banner\" style=\"display:block;\" class=\"bounceIn animated\" href=\"index.html\"> Loaded "+pk_len+" outfits</a>");
        setTimeout(fade_out, 3000);

    }

}

function fade_out() {
  $("#new-msg-container").fadeOut().empty();
}

function getUpdate(){
    $.ajax({
        url: "/OOTD/get-list-json/"+max_pk,
        dataType: "json",
        success : updateOutfit
    });
}

function updateOutfit(posts){
	if($(posts).length) {
		$("#new-msg-container").empty().css("display","block").append(
			"<a id=\"new-msg-banner\" style=\"display:block;\" class=\"bounceIn animated\" href=\"index.html\"><span> New Outfit. Refresh to see </span></a>");
	}

	// if($(posts).length){
	// 	$(posts).each(function(){

	// 		// getTags(this.fields.pk);

	// 		var tag_btn_id = "outfit-id-"+this.pk;

	// 		$("#fh5co-board .column:first").prepend(
	// 			"<div class=\"item\" id=\"outfit-item-"+this.pk+"\">" +
	// 			"<div class=\"animate-box bounceIn animated\">"+
	// 			"<a id=\"outfit-container-"+this.pk+"\" href=\"/OOTD/photo/"+this.pk+"\" class=\"image-popup fh5co-board-img\">" +
	// 								"<img id=\"outfit-picture-"+this.pk+"\" src=\"/OOTD/photo/"+this.pk+"\" alt=\"Free HTML5 Bootstrap template\">"+
	// 							"</a>"+
	// 							"<div class=\"planetmap\">"+
	// 							"</div>"+
	// 							"<img id=\"outfit-id-"+this.pk+"\" style=\"max-width:100px; height:auto\" class=\"tag_btn\" src=\"/static/images/tag_btn.png\" onclick=\"showTags("+tag_btn_id+")\" ></div>"+
	// 							"<div class=\"fh5co-desc\"><a href=\"/OOTD/profile/"+this.fields.created_by[0]+"\">" +
	// 							this.fields.created_by[0]+"</a>" +
	// 							"<p >185cm Pittsburgh</p>"+
	// 							"<p style=\"margin:0px\" >"+
	// 							"<button id=\"outfit-like-"+this.pk+"\" value=\"0\" type=\"button\" onclick=\"like(this.id)\" class=\"btn btn-default btn-sm\">"+
 //          						"<span class=\"glyphicon glyphicon-heart-empty \" /><span class=\"likeno\"> "+this.fields.likes+"</span>"+
 //        						"</button>"+
 //        						"</p></div></div>");
	// 	});
	// 	console.log("updateOutfit max_pk=" + max_pk);
	// 	max_pk = posts[posts.length - 1].pk;
	// }
}

function showTags(id){
	var tmp = id.split("-");
	console.log(tmp);
	id = tmp[2] //id='clothes-id-{{cloth.id}}'

	if ($('#outfit-item-'+id+' .tagged_title').css('display') == 'block') {

    	$('#outfit-item-'+id+' .tagged_title').css("display","none");
		$('#outfit-item-'+id+' .tagged_circle').css("display","none");
	} else {
	    $('#outfit-item-'+id+' .tagged_title').css("display","block");
		$('#outfit-item-'+id+' .tagged_circle').css("display","block");

	}

}

function like(id){
	fullid = id;
	var tmp = id.split("-");
	id = tmp[2] //id="outfit-like-{{outfit.id}}" 
	if($("#"+fullid + " input")) {
		console.log("found");
	}
	var status = $("#"+fullid + " input").val();
	console.log(status);

	if (status == "0") {
		console.log("in 0" + status);
		$.ajax({
			url:"/OOTD/like/"+id,
			type:"POST",
	        data:"id="+id+"&csrfmiddlewaretoken="+getCSRFToken(),
			dataType:"json",
			success:function(data){}
		});
		$("#"+fullid + " input").val("1");
		$("#"+fullid+ " .glyphicon").addClass('glyphicon-heart').removeClass('glyphicon-heart-empty');
		var likes = parseInt($("#"+fullid +" .likeno").text());
		$("#"+fullid +" .likeno").text(" " + (likes+1))
	} else {
		$.ajax({
			url:"/OOTD/unlike/"+id,
			data:"id="+id+"&csrfmiddlewaretoken="+getCSRFToken(),
			type:"POST",
			dataType:"json",
			success:function(data){}
		});
		$("#"+fullid + " input").val("0");
		$("#"+fullid + " .glyphicon").addClass('glyphicon-heart-empty').removeClass('glyphicon-heart');
		var likes = parseInt($("#"+fullid +" .likeno").text());
		$("#"+fullid +" .likeno").text(" " + (likes-1))
	}
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


 window.onload = getInitPK;
// causes list to be re-fetched every 5 seconds
window.setInterval(getUpdate, 5000);
