$(document).ready(function(){

  var $container = $('.list')
  var $containerImage = $('.imageNavigation')
  var sectionSpacing = 7
  var thisSAVED;
  var scrollToIssue;
  var stringa;
  var delay=375;
  var setTimeoutConst;
  var toTopsetTimeoutConst;
  var hashOptions = window.location.hash.replace('#', '')


  $(window).load(function() {
    var sortAreaOffset = $("#sortArea").offset().top;
  })


  

  $('p.authorTitle').css({"margin-bottom":"4px"})


  function adjustIssues(){

    if($(window).width()>1024){
      $('.list li, .issue').css({"padding-left":"","margin-left":"", "width":""})     

    }else{
      $('.list li, .issue').css({"padding-left":"0px","margin-left":"0px", "width":"100%"})


    }

  }

  function toTop(){

    $(window).resize(function() {
        clearTimeout(toTopsetTimeoutConst);
        toTopsetTimeoutConst = setTimeout(doneResizing, 300);
        
    });

    function doneResizing(){
      $("html, body").animate({ scrollTop: "0" },200);
    }

  }


  function textImageNavigator(){
    var $checkboxes_textImage = $('.themes #textImage input');
          
      $checkboxes_textImage.change( function() {

            $('#textImage p').removeClass("underlineFilter")
            $('#textImage input').not(this).prop('checked', false);
            if($(this).prop('checked')==false){
              $('#textImage input').not(this).prop('checked', true);
              $('#textImage input').not(this).next("p").toggleClass("underlineFilter")
              $('input.'+$(this).attr("class")+'').next("p").toggleClass("underlineFilter")
            }
            $('input.'+$(this).attr("class")+'').next("p").toggleClass("underlineFilter")

            if($(window).width()>1024){
              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                })
                $containerImage.isotope({ 
                  itemSelector: 'li',
                })
              },10)

              $container.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })
              $containerImage.isotope({ 
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
              $containerImage.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })

              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                })
              $containerImage.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })
              },500)

              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                })
                $containerImage.isotope({ 
                  itemSelector: 'li',
                  filter: hashOptions
                })
              },1000)

              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                })
              $containerImage.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })
              },2000)

              calculateSection()
              calculateSectionNarrow()
            }
    }); 

  }

  function addTitleHoverImage(){
    $('.imageNavigation').children('li')
  .mouseover(function() {
    thisSAVED01 = $(this)
    stringa = thisSAVED01.attr('data-name')

    setTimeoutConst = setTimeout(function(){
          
          thisSAVED01.find('img').addClass('hoverImg')
          thisSAVED01.find('a').addClass('hoverImgLink')

          $('.imageNavigation').children('li').each(function(){
            if(stringa == $(this).attr('data-name')){
              $(this).find('img').addClass('hoverImg')
              $(this).find('a').addClass('hoverImgLink')
            }
          })

         thisSAVED01.append('<p class="title">'+stringa.replace(/_/g, ' ')+'</p>')
          $('.imageNavigation').isotope()
    }, delay);

  })
  .mouseout(function() {
     clearTimeout(setTimeoutConst );
    $('.imageNavigation').children('li').each(function(){
      if(stringa == $(this).attr('data-name')){
        $(this).find('a').removeClass('hoverImgLink')
        $(this).find('img').removeClass('hoverImg')
      }
    })
      
    thisSAVED01.find('.title').remove()
    $('.imageNavigation').isotope()
  });

  }

  addTitleHoverImage()

  toTop()

  function calculateSection(){

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

  if ($('#textImage input:checked').next('p').text() == "Title"){
      $('.list').children('li').find('a').fadeIn(500)
      $('.list').children('li').find('p').fadeIn(500)
      $('.issue').removeClass('issueImage')
      $('.imageNavigation').hide()
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

      })
      $(".section-wide").fadeIn(500)
  

    } else{
      $('.list').children('li').children().hide()
      $('.imageNavigation').fadeIn(500)
      $('.issue').addClass('issueImage')
      $(".section-div").remove()
    }

  }


    function calculateSectionNarrow(){

      if ($('#textImage input:checked').next('p').text() == "Title"){

      $('.list').children('li').find('a').fadeIn(1500)
      $('.issue').removeClass('issueImage')
      $('.imageNavigation').hide()
      $('.section-wide').css({"display":"none"})
      $(".section-narrow").fadeIn(500)

          } else{

          $('.list').children('li').children().hide()
          $('.imageNavigation').fadeIn(1500)
          $('.issue').addClass('issueImage')
          $(".section-div").remove()
        }

  }

  setTimeout(function(){
   $('#textImage input').each(function(){
    if ($(this).prop('checked')==true){
      $(this).next("p").toggleClass("underlineFilter")
    }
   })

  startfilter = window.location.hash.replace('#', '')
  startfilterArray = startfilter.split(".")
  startfilterArray.shift()

  startfilterArray.forEach(function(afilter) {
      $('input.'+afilter+'').next("p").toggleClass("underlineFilter")
      $('input.'+afilter+'').prop('checked', $(this).is(':checked'));
      $('input.'+afilter+'').prop( "checked", true )
  });



    if($(window).width()>1024){


      $container.isotope({ 
        itemSelector: 'li',
        filter: hashOptions
      })
      $containerImage.isotope({ 
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
      $containerImage.isotope({ 
        itemSelector: 'li',
        filter: hashOptions
      })

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
        })
      },500)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
        })
      },1000)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
        })
      },2000)

      calculateSection()
      calculateSectionNarrow()
    }

    textImageNavigator()


    var $checkboxes = $('.themes #sortTopics input');
        
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
          $checkboxes.each( function( i, elem ) {
            if ( elem.checked ) {
              exclusives.push( elem.value );
            }
          });

          exclusives = exclusives.join('');
          
          var filterValue;
          filterValue = exclusives;

          location.hash = filterValue

          hashOptions = window.location.hash.replace('#', '')


          $container.isotope({ 
            itemSelector: 'li',
            filter: hashOptions
          })


          $containerImage.isotope({ 
              itemSelector: 'li',
              filter: hashOptions
            })

          if($(window).width()>1024){

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                })
            },500)

          }else{

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                })
            },500)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                })
            },1000)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                })
            },2000)

          }


          $(window).scrollTop(scrollFromTop)

    }); 

    $(window).scroll(function(){
        if ($(window).scrollTop() > sortAreaOffset) {
          $("#sortArea").addClass("fixedSort")
          $(".issueWrapper").css({"margin-top":$("#sortArea").outerHeight()+"px"})

        } else{
          $("#sortArea").removeClass("fixedSort")
          $(".issueWrapper").css({"margin-top":"0px"})
        }
    
    });


  },400);
  
  sortAreaOffset = $("#sortArea").offset().top

  $(window).resize(function(){

    // sortAreaOffset = $("#sortArea").offset().top

    if($(window).width()>1024){

    calculateSectionWide()

    }else{

    calculateSectionNarrow()

    }

    adjustIssues()

  })

  adjustIssues()


})
