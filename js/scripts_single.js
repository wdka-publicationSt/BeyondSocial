// $(window).load(function() {

//  // executes when complete page is fully loaded, including all frames, objects and images
//  //alert("window is loaded");
//  console.log($(document).outerHeight(true))
//  console.log($(document).height())
// });
var savedContent;
var flip;

$('document').ready(function() {
	
		if ($(window).width()>1024){
			flip = true
		}else{
			flip = false
		}

		// $(window).load(function($){
		// 	console.log("hiiaaaaaaaaaaa")
		// 	console.log($('.content').height())
		// })
		var savedContent = $('.content').html()

		function initLayout(){

			if($('figure').length>0){

				console.log('has images')

				if ($(window).width()>1024 && flip == true){

					$('.content').removeClass('fullWidth')
					$('figure').css({"display":"block"})

					$('.content').before('<div class="attachment"></div>')

					$('figure').appendTo('.attachment')

					$(".attachment").css({"height":$('.content').height()+"px"})

					$.fn.vAlign = function() {
							return this.each(function(i){
						var ah = $(this).height();
						var ph = $(this).parent().height();
						var mh = Math.ceil((ph-ah) / ($("figure").length*2));
						$(this).css('margin-bottom', mh);
						});
					};
				
					
					$('.content').show()
					$(".attachment figure").vAlign()

					flip = false
				} 

				if ($(window).width()<=1024 && flip == false){
					
					$('.attachment').remove()
					$('.content').html(savedContent)
					$('.content').addClass('fullWidth')
					$('figure').css({"display":"inline"})
					$('.content').show()
		
					flip = true
				} 

				// else {
				// 	//flip = true;
				// 	console.log("smallllllller than")
				// 	console.log(flip)
				// 	$('.attachment').remove()
				// 	$('.content').html(savedContent)
				// 	$('.content').addClass('fullWidth')
				// 	$('.content').show()
					
				// }	


				$('figcaption').each(function(){
						$(this).css({"width":$(this).prev().width()+"px"})
				})

			}

			else{

				$('.content').css({"width":"100%","display":"block"})
			}

		}
		

		$(window).resize(function(){
			initLayout()
		})

		// var img = $("img")[0]; // Get my img elem
		// var pic_real_width, pic_real_height;
		// $("<img/>") // Make in memory copy of image to avoid css issues
		//     .attr("src", $(img).attr("src"))
		//     .load(function() {
		//         pic_real_width = this.width;   // Note: $(this).width() will not
		//         pic_real_height = this.height; // work for in memory images.
		//         console.log(pic_real_height)
		//   })

		$(window).load(function() {
				   initLayout()
		});

});
