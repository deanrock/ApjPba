/* Subject */
$(document).ready(function() {
	$('input[name=\'show_subject\']').click(function() {
		if($(this).val() == "") {
			window.location.href = "?";
		}else{
			window.location.href = "?subject=" + $(this).val();
		}
	});
});


			

var scroll_on_load = false;

//login
function login_submit() {
username = $("#login_username").val();
password = $("#login_password").val();
$("#content_login").html('<p align="center"><img src="/images/ajax-loader.gif" /></p>');
$.ajax({
   type: "POST",
   url: "/login?ajax=1",
cache: false,
   data: ({ 
		'username': username, 
		'password': password
		}),
   success: function(msg){
	if(msg=="redirect") {
		location.href = "/";
	}else{
     $("#content_login").html(msg);
	}
   }
 });

}

//index
function load_question(id, div) {
if($("#"+div).is(":hidden")) {
	$(".q_div").slideUp("slow");
	//$("#"+div).html('<p align="center"><img src="/images/ajax-loader.gif" /></p>');
	
	
	$.ajax({
	   type: "POST",
	   url: "/question",
		cache: false,
	   data: ({ 
			'id': id,
			'div': div,
			'csrfmiddlewaretoken': csrf_token
			}),
	   success: function(msg){
	     $("#"+div).html(msg);
$("#"+div).slideDown("slow");
			
		//	if(scroll_on_load) {
				$('html, body').animate({
				scrollTop: $("#"+div).offset().top-200
				}, 2000);
				
		//	}
	   }
	 });
}else{
	$("#"+div).slideUp("slow");
}
}

function edit_question(id, div) {
	location.href = "/answers/edit/"+id;
}

function show_category(id) {
	if($("#category_content_"+id).is(":hidden")) {
	$(".c_div").slideUp("slow");
	$("#category_content_"+id).slideDown("slow");
	}else{
		$("#category_content_"+id).slideUp("slow");
	}
}

function redirect_login() {
	location.href = "/login";
}

function getHash() {
  var hash = window.location.hash;
  return hash.substring(1); // remove #
}



$(document).ready(function(){
			$(".ajax").colorbox();

	hash = getHash();
	
	x=hash.split('_');

	if(x.length > 3) {
		cat = x[1];
		que = x[2];
		id = x[3];

		//load cat,que
		show_category(cat);
scroll_on_load=true;
		load_question(id, 'question_'+cat+'_'+que);

		
	}
});



//edit
function hide_file(id, file) {
	$.ajax({
	   type: "POST",
	   url: "/answers/hide_file",
		cache: false,
	   data: ({ 
			'id': id,
			'file': file,
			'csrfmiddlewaretoken': csrf_token
			}),
	   success: function(msg){
	     $("#edit_show_pictures").html(msg);
	   }
	 });
}

function show_file(id, file) {
	$.ajax({
	   type: "POST",
	   url: "/answers/hide_file",
		cache: false,
	   data: ({ 
			'id': id,
			'file': file,
			'show' : 1,
			'csrfmiddlewaretoken': csrf_token
			}),
	   success: function(msg){
	     $("#edit_show_pictures").html(msg);
	   }
	 });
}