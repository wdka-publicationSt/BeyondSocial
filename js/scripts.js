$(document).ready(function(){

  var $container = $('.list')
  var sectionSpacing = 7
  var thisSAVED;
  var scrollToIssue;
  var hashOptions = window.location.hash.replace('#', '')
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

  startfilter = window.location.hash.replace('#', '')
  startfilterArray = startfilter.split(".")
  startfilterArray.shift()

  startfilterArray.forEach(function(afilter) {
      // console.log('//////////////////////////////////////');
      // console.log(afilter);
      $('input.'+afilter+'').next("p").toggleClass("underlineFilter")
      $('input.'+afilter+'').prop('checked', $(this).is(':checked'));
      $('input.'+afilter+'').prop( "checked", true )
  });



    if($(window).width()>1024){


      $container.isotope({ 
        itemSelector: 'li',
        filter: hashOptions
      })
      calculateSection()
      calculateSectionWide()

    }else{


      $container.isotope({ 
        itemSelector: 'li',
        filter: hashOptions
      })

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
          // filter: hashOptions
        })
      },500)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
          // filter: hashOptions
        })
      },1000)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
          // filter: hashOptions
        })
      },2000)

      calculateSection()
      calculateSectionNarrow()
    }

    var $checkboxes = $('.themes input');
        
      $checkboxes.change( function() {

      scrollFromTop = $(window).scrollTop()

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
          //var inclusives = [];

          // inclusive filters from checkboxes
          $checkboxes.each( function( i, elem ) {
            // if checkbox, use value if checked
            if ( elem.checked ) {
              //  inclusives.push( elem.value );

              exclusives.push( elem.value );
            }
          });

          //console.log(inclusives)
          // console.log(exclusives)
          // combine exclusive and inclusive filters
          // first combine exclusives
          exclusives = exclusives.join('');
          
          var filterValue;
          filterValue = exclusives;
          // if ( inclusives.length ) {
          //   // map inclusives with exclusives for
          //   filterValue = $.map( inclusives, function( value ) {
          //     return value + exclusives;
          //   });
          //   filterValue = filterValue.join(', ');
          // } else {
          //   filterValue = exclusives;
          // }

          //$.bbq.pushState();
          //filterValue = filterValue.replace('+', ' ').replace('#', '').replace('=', '')
          //$.bbq.pushState(filterValue);
          location.hash = filterValue
          //hashOptions = window.location.hash.replace('+', ' ').replace('#', '').replace('=', '')
          hashOptions = window.location.hash.replace('#', '')

            // do not animate first call
           
            // apply defaults where no option was specified

        // apply options from hash
          //$container.isotope( options );

          $container.isotope({ 
            itemSelector: 'li',
            filter: hashOptions
          })


          if($(window).width()>1024){

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
            },500)

          }else{

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
            },500)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
            },1000)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
            },2000)

          }


          $(window).scrollTop(scrollFromTop)

    }); 

    $(window).scroll(function(){
        // console.log(sortAreaOffset)
        if ($(window).scrollTop() > sortAreaOffset) {
          $("#sortArea").addClass("fixedSort")
          $(".issueWrapper").css({"margin-top":$("#sortArea").outerHeight()+"px"})

        } else{
          $("#sortArea").removeClass("fixedSort")
          $(".issueWrapper").css({"margin-top":"0px"})
        }
    
    });

  // $('input.'+'Politics'+'').next("p").toggleClass("underlineFilter")
  // $('input.'+'Politics'+'').prop('checked', $(this).is(':checked'));


  },400);
  
  sortAreaOffset = $("#sortArea").offset().top

  $(window).resize(function(){

    $("html, body").animate({ scrollTop: "0" },200);

    sortAreaOffset = $("#sortArea").offset().top
    // console.log(sortAreaOffset)

    if($(window).width()>1024){

    calculateSectionWide()

    }else{

    calculateSectionNarrow()

    }


    adjustIssues()

  })

  adjustIssues()


})
