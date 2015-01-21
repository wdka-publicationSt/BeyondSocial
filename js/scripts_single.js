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

	$('.articleHeader').find('p').each(function(){
		$(this).html($(this).html().replace("Issue_", ""))
	})

    
    $('.content').append('<figcaption class="currentArticleUrl" >Read online at:<br>http://www.beyond-social.org</figcaption>')

    $('.content').append('<br class="blankSpaceEnd">')

    $('.content').attr('lang','en')
    $('.content').find('a').each(function(){
    	//$(this).attr('href')
    	// alert($(this).attr('href'))
    	if ($(this).attr('title')=='wikilink'){
    		$(this).remove()
    	}
    	href = $(this).attr('href')
    	$(this).append("<a class='hrefPrint'> ("+href+")</a>")
    })
	$('p.av').each(function(){
	$(this).replaceWith($('<figcaption>' + this.innerHTML + '</figcaption>'));
	})

	$("h2:contains('Author:')").each(function(){
	authorRemove = $(this).text().replace(/Author:/g, "By:");
	quotesRemove = authorRemove.replace(/"/g, "");
	$(this).text(quotesRemove)
	})


	$('.av').wrap("<figure></figure>")
	$('iframe').wrap("<figure></figure>")

	if ($('html').width()>1024){
		flip = true
	}else{
		flip = false
	}

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

				$('figcaption').each(function(){
						$(this).css({"width":$(this).prev().width()+"px"})
				})

			}

			else{

				$('.content').css({"width":"100%","display":"block"})
			}

		}
		
		function imagesNotWide(){
			$('img').each(function(){
				width = $(this).width()
				height = $(this).height()
				if (width<height){
					console.log('high')
					$(this).parent().addClass('highImage')
				}
				if (width==height){
					console.log('sqiare')
					$(this).parent().addClass('squareImage')
				}
			})	
		}

		$(window).resize(function(){
			initLayout()
			imagesNotWide()

		})

		$(window).load(function() {
				   initLayout()
				   imagesNotWide()

				// if (h3offset < 1700){
				// 	$(this).next('p').andSelf().wrapAll('<div style="display:inline-block" class="formItem"/>');
				// 	//$(this).next("p").wrapAll('<div style="display=inline-block">')
				// 	alert('hi')
				// }
		});

		/// DETECT BEFORE AND AFTER PRINT

		var beforePrint = function() {

			// 1750,3800,5850,7900,9950,12000,14050,16100

			// var arrayValue = []
			// for (var i = 0; i < 40; i++) {
			// 	arrayValue.push(30+1470*i)
			// }	
			// console.log(arrayValue)
			
		    // $('html').css({"width":"676px"})
		    $('html').css({"width":"718px"})


		    $(window).resize()

		    $('iframe').hide()
		    $('figure').has('iframe').each(function(){
		    	$(this).append("<div class='blankImageDiv'><figcaption class='videoPlaceholder'>Video available at: "+$(this).children('iframe').attr('src')+"</figcaption></div>")
		    	//$(this).append("<div class='blankImageDiv'></div><figcaption class='videoPlaceholder'>Video available at: "+$(this).children('iframe').attr('src')+"</figcaption>")
		    })


			// $('.content').find('h3').each(function(){		
				
			// 	for (var i = 0; i < arrayValue.length; i++) {
			// 		h3offset = $(this).offset().top-$('.content').offset().top

			// 		if (h3offset > (arrayValue[i]-300) && h3offset < (arrayValue[i]+300)){
			// 			$(this).next('p').andSelf().wrapAll('<div style="display:inline-block" class="formItem"/>');

			// 		}    
			// 	}
			// })

		};
		var afterPrint = function() {
			$('html').css({"width":"auto"})
			$(window).resize()

			$('iframe').show()
			$('.videoPlaceholder').remove()

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

