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
    	$(this).append("<a class='hrefPrint' style='font-size:inherit !important; word-break:break-all !important; white-space: pre-wrap  !important; white-space: -moz-pre-wrap  !important; word-wrap: break-word  !important;'>&nbsp;("+href+")</a>")
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


		/// DETECT BEFORE AND AFTER PRINT

		var beforePrint = function() {


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

