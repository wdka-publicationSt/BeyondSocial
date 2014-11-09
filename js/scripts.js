$(document).ready(function(){

  var $container = $('.list')
  var sectionSpacing = 7
  var thisSAVED;
  var scrollToIssue;
  // var sortAreaOffset = $("#sortArea").offset().top;
  $(window).load(function() {
    var sortAreaOffset = $("#sortArea").offset().top;
  })
  
  function adjustIssues(){

    if($(window).width()>1024){
      $('.list li, .issue').css({"padding-left":"","margin-left":"", "width":""})     

    }else{
      $('.list li, .issue').css({"padding-left":"0px","margin-left":"0px", "width":"100%"})


    }

  }


  function calculateSection(){

    //$(".section-div").remove()

      $container.each(function(){
      

        $(this).children("li:visible").each(function(){
          section = $(this).attr("data-section")

          
          if ($(this).prevAll("li:visible:first").attr("data-section") != section){
            $(this).prepend("<div class='section-div section-narrow'>"+section+"</div>")
            $(this).prepend("<div class='section-div section-wide'>"+section+"</div>")
          }

        })


      })

  }


  function calculateSectionWide(){

    //$(".section-div").remove()

      $('.section-narrow').css({"display":"none"})

      $container.each(function(){
        
        //// GET TOTAL HEIGHT OF SECTION ////
        jsonHeight = []

        $(this).children("li:visible").each(function(){
          section = $(this).attr("data-section")
          jsonVariable = {}
          jsonVariable[section] = $(this).height()
          
          jsonHeight.push(jsonVariable);
        })

        //// ATTACH SECTION DEVIDER TO FIRST LI IN SECTION ////

        $(this).children("li:visible").each(function(){
          section = $(this).attr("data-section")
          totalH = 0 
          for (var i = 0; i < jsonHeight.length; i++) {
            if (isNaN(jsonHeight[i][section]) == false){   
              totalH = totalH + jsonHeight[i][section]
            }
          }
          if ($(this).prevAll("li:visible:first").attr("data-section") != section){
            $(this).find(".section-wide").css({"height":totalH-sectionSpacing+"px", "line-height":totalH-sectionSpacing+"px"})
          }

        })

        //$(".section-div").fadeIn(250)

      })
      //$('.section-wide').css({"display":"block"})
      $(".section-wide").fadeIn(500)
      

  }


    function calculateSectionNarrow(){

      $('.section-wide').css({"display":"none"})
      $(".section-narrow").fadeIn(500)
      //$('.section-narrow').css({"display":"table"})


  }

  setTimeout(function(){

    if($(window).width()>1024){

      calculateSection()
      calculateSectionWide()
      $container.isotope({
          itemSelector: 'li'
      })

    }else{

      calculateSection()
      calculateSectionNarrow()
      $container.isotope({
          itemSelector: 'li'
      })
    }

    var $checkboxes = $('.themes input');
        
      $checkboxes.change( function() {
      


        $container.isotope( 'on', 'layoutComplete', function() {

          $(".section-div").remove()

                calculateSection()

                if($(window).width()>1024){

                calculateSectionWide()

                }else{

                calculateSectionNarrow()

                }
        
        });


          var checkboxesCheck = $('.themes input:checked');

          thisSAVED = $(this).parents(".issueWrapper")

          $('input.'+$(this).attr("class")+'').next("p").toggleClass("underlineFilter")
          $('input.'+$(this).attr("class")+'').prop('checked', $(this).is(':checked'));
         
          var exclusives = [];
          var inclusives = [];

          // inclusive filters from checkboxes
          $checkboxes.each( function( i, elem ) {
            // if checkbox, use value if checked
            if ( elem.checked ) {
              inclusives.push( elem.value );
              exclusives.push( elem.value );
            }
          });

          // combine exclusive and inclusive filters
          // first combine exclusives
          exclusives = exclusives.join('');
          
          var filterValue;
          if ( inclusives.length ) {
            // map inclusives with exclusives for
            filterValue = $.map( inclusives, function( value ) {
              return value + exclusives;
            });
            filterValue = filterValue.join(', ');
          } else {
            filterValue = exclusives;
          }

          $container.isotope({ 
            filter: filterValue 
          })

          if($(window).width()>1024){

            setTimeout(function(){
              $container.isotope({
                itemSelector: 'li'
              })
            },500)

          }else{

            setTimeout(function(){
              $container.isotope({
                itemSelector: 'li'
              })
            },500)

            setTimeout(function(){
              $container.isotope({
                itemSelector: 'li'
              })
            },1000)

            setTimeout(function(){
              $container.isotope({
                itemSelector: 'li'
              })
            },2000)

          }




    });


    

    $(window).scroll(function(){
          console.log(sortAreaOffset)
        if ($(window).scrollTop() > sortAreaOffset) {
          $("#sortArea").addClass("fixedSort")
          $(".issueWrapper").css({"margin-top":$("#sortArea").outerHeight()+"px"})

        } else{
          $("#sortArea").removeClass("fixedSort")
          $(".issueWrapper").css({"margin-top":"0px"})
        }
    
    });


  },400);


  $(window).resize(function(){

    sortAreaOffset = $("#sortArea").offset().top
    console.log(sortAreaOffset)

    if($(window).width()>1024){

    calculateSectionWide()

    }else{

    calculateSectionNarrow()

    }


    adjustIssues()

  })

  adjustIssues()


})
