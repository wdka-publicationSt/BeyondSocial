$(document).ready(function(){

  var $container = $('.list')
  var $containerImage = $('.imageNavigation')
  var sectionSpacing = 7
  var thisSAVED;
  var scrollToIssue;
  var hashOptions = window.location.hash.replace('#', '')
  // var sortAreaOffset = $("#sortArea").offset().top;
  $(window).load(function() {
    var sortAreaOffset = $("#sortArea").offset().top;
  })
  

// $('#textImage input').prop('checked', false);

// $('#textImage .Text').prop('checked', true);

  function adjustIssues(){

    if($(window).width()>1024){
      $('.list li, .issue').css({"padding-left":"","margin-left":"", "width":""})     

    }else{
      $('.list li, .issue').css({"padding-left":"0px","margin-left":"0px", "width":"100%"})


    }

  }


  function textImageNavigator(){
    var $checkboxes_textImage = $('.themes #textImage input');
          
      $checkboxes_textImage.change( function() {

            $('#textImage p').removeClass("underlineFilter")
            $('#textImage input').not(this).prop('checked', false);
            // console.log($(this).prop('checked'))
            if($(this).prop('checked')==false){
              $('#textImage input').not(this).prop('checked', true);
              $('#textImage input').not(this).next("p").toggleClass("underlineFilter")
              $('input.'+$(this).attr("class")+'').next("p").toggleClass("underlineFilter")
            }
            // $('#textImage input').not(this).prop('checked', false);
            $('input.'+$(this).attr("class")+'').next("p").toggleClass("underlineFilter")

            if($(window).width()>1024){
              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                  // filter: hashOptions
                })
                $containerImage.isotope({ 
                  itemSelector: 'li',
                  // filter: hashOptions
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
                  // filter: hashOptions
                })
              $containerImage.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })
              },500)

              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                  // filter: hashOptions
                })
                $containerImage.isotope({ 
                  itemSelector: 'li',
                  filter: hashOptions
                })
              },1000)

              setTimeout(function(){
                $container.isotope({ 
                  itemSelector: 'li',
                  // filter: hashOptions
                })
              $containerImage.isotope({ 
                itemSelector: 'li',
                filter: hashOptions
              })
              },2000)

              calculateSection()
              calculateSectionNarrow()
            }


         
          //   if($(this).next("p").text() == 'Image'){
          //     // alert('hi')
          //     $('.section-div').remove()
          //   }

          // $('#textImage input:checked').each(function() {
          //   chkArray.push($(this).val());
          // });



    }); 

  }

// console.log('hiiiiiiiiii')
  function addTitleHoverImage(){
    $('.imageNavigation').children('li')
  .mouseover(function() {
    stringa = $(this).attr('data-name')
    // $(this).find('img').addClass('hoverImg')
    // $(this).find('a').addClass('hoverImgLink')

    $('.imageNavigation').children('li').each(function(){
      if(stringa == $(this).attr('data-name')){
        console.log('same')
        $(this).find('img').addClass('hoverImg')
        $(this).find('a').addClass('hoverImgLink')
      }
    })

    $(this).append('<p class="title">'+stringa.replace(/_/g, ' ')+'</p>')
    $('.imageNavigation').isotope()
    // alert('over')
  })
  .mouseout(function() {
    // alert('out')

    $('.imageNavigation').children('li').each(function(){
      if(stringa == $(this).attr('data-name')){
        console.log('same')
        $(this).find('a').removeClass('hoverImgLink')
        $(this).find('img').removeClass('hoverImg')
      }
    })
    
    $(this).find('.title').remove()
    $('.imageNavigation').isotope()
  });

  }

  addTitleHoverImage()

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

      //$('.list').children('li').children('a').show()
      // $('.list').children('li').children('a:has(*)').hide()


  if ($('#textImage input:checked').next('p').text() == "Title"){

      // $('.list li').removeClass('liNoMargin')
      // $('.list').removeClass('ulNoMargin')

      // $('.list').children('li').children('a:not(:has(*))').show()
      // $('.list').children('li').children('a:has(*)').hide()
      $('.list').children('li').find('a').fadeIn(500)
      $('.issue').removeClass('issueImage')
      $('.imageNavigation').hide()


      $('.list').children('li').children('a').children('p').show()
      $('.list').children('li').children('a').children('img').hide()
      $('.list').children('li').removeClass('imageSorting')
              // setTimeout(function(){
              //   $container.isotope({ 
              //     itemSelector: 'li',
              //     // filter: hashOptions
              //   })
              // },500)

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
      console.log('text')
      //$('.section-wide').css({"display":"block"})
      $(".section-wide").fadeIn(500)
  

    } else{

      console.log('image')

      // $('.list').children('li').children().hide()
      // $('.list').children('li').children('a:not(:has(*))').hide()
      // $('.list').children('li').children('a:has(*)').show()
      // $('.list').children('li').children('a:has(*)').show()
      // $('.imageNavigation').fadeIn(500)
      
      $('.issue').addClass('issueImage')


      // $('.list li').addClass('liNoMargin')
      // $('.list').addClass('ulNoMargin')

      // $('.list').children('li').children('a:not(:has(*))').hide()
      $('.list').children('li').addClass('imageSorting')
      $('.list').children('li').children('a').children('p').hide()
      $('.list').children('li').children('a').children('img').show()
      $(".section-div").remove()
    }

  }


    function calculateSectionNarrow(){

      if ($('#textImage input:checked').next('p').text() == "Text"){

      $('.list').children('li').find('a').fadeIn(1500)
      $('.issue').removeClass('issueImage')
      // $('.imageNavigation').hide()

      //$('.list').children('li').children('a').show()
      // $('.list').children('li').children('a:has(*)').hide()


      $('.section-wide').css({"display":"none"})
      $(".section-narrow").fadeIn(500)
      //$('.section-narrow').css({"display":"table"})
      console.log('text')

          } else{

          console.log('image')

          // $('.list').children('li').children().hide()
          // $('.list').children('li').children('a:not(:has(*))').hide()
          // $('.list').children('li').children('a:has(*)').show()
          // $('.list').children('li').children('a:has(*)').show()
          // $('.imageNavigation').fadeIn(1500)
          $('.issue').addClass('issueImage')


          // $('.list li').addClass('liNoMargin')
          // $('.list').addClass('ulNoMargin')

          // $('.list').children('li').children('a:not(:has(*))').hide()
          $(".section-div").remove()
        }

  }
  //   } else{

  //     console.log('image')
  //     // $('.list').children('li').children('a:not(:has(*))').hide()
  //     $(".section-div").remove()
  //   }

 

  setTimeout(function(){

    // $('#textImage input').prop('checked', false);


   $('#textImage input').each(function(){
    if ($(this).prop('checked')==true){
      $(this).next("p").toggleClass("underlineFilter")
    }
   })

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
          // filter: hashOptions
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
          //filter: hashOptions
        })
      },500)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
          // filter: hashOptions
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
          //filter: hashOptions
        })
      },1000)

      setTimeout(function(){
        $container.isotope({ 
          itemSelector: 'li',
          // filter: hashOptions
        })
        $containerImage.isotope({ 
          itemSelector: 'li',
          //filter: hashOptions
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
          //var inclusives = [];

          // inclusive filters from checkboxes
          $checkboxes.each( function( i, elem ) {
            // if checkbox, use value if checked
            if ( elem.checked ) {
              //  inclusives.push( elem.value );

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
                // filter: hashOptions
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                  //filter: hashOptions
                })
            },500)

          }else{

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                  //filter: hashOptions
                })
            },500)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                  //filter: hashOptions
                })
            },1000)

            setTimeout(function(){
              $container.isotope({ 
                itemSelector: 'li',
                // filter: hashOptions
              })
              $containerImage.isotope({ 
                  itemSelector: 'li',
                  //filter: hashOptions
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
