// $(window).load(function() {

//  // executes when complete page is fully loaded, including all frames, objects and images
//  //alert("window is loaded");
//  console.log($(document).outerHeight(true))
//  console.log($(document).height())
// });
var savedContent;
var flip;

$('document').ready(function() {
    $('a[title=wikilink]:contains("Category:")').hide(); // hide categories at bottom of page
		$('p.av').each(function(){
		$(this).replaceWith($('<figcaption>' + this.innerHTML + '</figcaption>'));
		})

		$('.av').wrap("<figure></figure>")
		$('iframe').wrap("<figure></figure>")
	
		if ($('html').width()>1024){
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

			//if($('figure').length>0 || $('.av').length>0 || $('iframe').length>0){
			if($('figure').length>0){

				console.log('has images')

				if ($('html').width()>1024 && flip == true){

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

				if ($('html').width()<=1024 && flip == false){
					
					$('.attachment').remove()
					$('.content').html(savedContent)
					$('.content').addClass('fullWidth')
					// $('figure').css({"display":"inline"})
					//$('audio').css({"display":"inline"})
					//$('iframe').css({"display":"inline"})
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

				// if (h3offset < 1700){
				// 	$(this).next('p').andSelf().wrapAll('<div style="display:inline-block" class="formItem"/>');
				// 	//$(this).next("p").wrapAll('<div style="display=inline-block">')
				// 	alert('hi')
				// }
		});



		var beforePrint = function() {

			// 1750,3800,5850,7900,9950,12000,14050,16100

			var arrayValue = []
			for (var i = 0; i < 40; i++) {
				arrayValue.push(1750+(2050*i))
			}
			// console.log(arrayValue[2])
			
		    // $('html').css({"width":"676px"})
		    $('html').css({"width":"718px"})
		    $(window).resize()
			$('.content').find('h3').each(function(){		
				
				for (var i = 0; i < arrayValue.length; i++) {
					h3offset = $(this).offset().top-$('.content').offset().top

					if (h3offset > (arrayValue[i]-100) && h3offset < (arrayValue[i]+100)){
						$(this).next('p').andSelf().wrapAll('<div style="display:inline-block" class="formItem"/>');

					}    
				}
			})

		};
		var afterPrint = function() {
			$('html').css({"width":"auto"})
			$(window).resize()
		};


		if (window.matchMedia) {
		    var mediaQueryList = window.matchMedia('print');
		    mediaQueryList.addListener(function(mql) {
		        if (mql.matches) {
		            beforePrint();
		        } else {
		            afterPrint();
		        }
		    });
		}

		window.onbeforeprint = beforePrint;
		window.onafterprint = afterPrint;


});

