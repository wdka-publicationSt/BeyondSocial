function shareClick(){
 
  $(document).on('click','#shareButtons a', function(e){
    e.preventDefault()
    var currentUrl=window.location.href
    if($(this).attr('id') == 'shareTwitter'){
      window.open('https://twitter.com/intent/tweet?text='+currentUrl); 
    }else if($(this).attr('id') == 'shareFacebook'){
      window.open('https://www.facebook.com/sharer/sharer.php?u='+currentUrl); 
    }
  })

}

function addFBImage(){
  if($('.content').find('img').length == true){
    $('head').append('<link rel="image_src" type="image/jpeg" href="'+$('.content').find('img').first()[0].src+'" />')
    // $('head').append('<link rel="image_src" type="image/jpeg" href="http://template01.info/index/media/aaaanB01.jpg" />')

  }else{
    $('head').append('<link rel="image_src" type="image/jpeg" href="'+$(document).find('img').first()[0].src+'" />')
    // $('head').append('<link rel="image_src" type="image/jpeg" href="http://template01.info/index/media/aaaanB01.jpg" />')
  // }
  }
}


function clickAbout(){
  $(document).on('click','#toAbout', function(){
    window.location.href = 'articles/Issue3-test-article-2.html';
    // $("html, body").animate({ scrollTop: $(document).height() },200);
  })
}

function clickTop(){
  $(document).on('click','#toTop', function(){
    $("html, body").animate({ scrollTop:0},200);
  })
}





$(document).ready(function(){
  shareClick()
  clickAbout()
  clickTop()
  addFBImage()
}); 