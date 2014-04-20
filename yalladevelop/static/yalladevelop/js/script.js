$(document).ready(function(){
	
});

function readURL(input){
	if (input.files && input.files[0]){
		var reader = new FileReader();
		reader.onload = function (e){
			$('#user_image_preview').val("<img class=\"img-circle\" src=\"" + e.target.result + "\"/>");
		}		
		reader.readAsDataURL(input.files[0]);
	}
}

$('#image').change(function(){
	readURL(this);
});

// function initDragDrop(){
// 	var zone = $("#user_upload")[0];
// 	zone.ondragstart = function(){return false;};
// 	zone.ondragend = function(){return false;};
// 	zone.ondragover = function(){return false;};
// 	zone.ondragenter = function(){return false;};
// 	zone.ondragleave = function(){return false;};
// 	zone.ondrop = function(e){
// 		e.preventDefault();
// 		document.getElementById("user_image_preview").innerHTML=''; // removing current preview if exists
// 		var file = e.dataTransfer.files[0]; // accepting the first image only
// 		var reader = new FileReader();
// 		reader.onload = function (e) {
// 			var str = e.target.result;
// 			if (str.slice(5,10) != "image"){ // only allowing Images to be uploaded, not any other files
// 				alert("You are only allowed to upload images on this form, please check the format of the image and make sure you submit an image with a proper format.");
// 				return false;
// 			}
//             $("#user_image_preview").append("<img class=\"img-circle\" src=\"" + e.target.result + "\"/>");
// 			// $("#user_uploader").append("<input type=\"hidden\" name=\"profile_picture\">"+e.target.result+"</input>");
// 			// $("#user_picture").val(e.target.result);
// 			$("input[name=image]").val(e.target.result);
// 			// $("input[name=imgg]").val(e.target.result);
// 						
// 			$('input[type=file]').change(function () {
// 			    console.log(this.files[0].mozFullPath);
// 			});
// 			
// 			//console.log($("input[name=image]")[0].defaultValue);
// 		};
// 		reader.readAsDataURL(file);
// 		return false;
// 	};
// }

