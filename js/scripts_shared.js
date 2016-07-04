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
function clickAbout(){
  $(document).on('click','#toAbout', function(){
    $("html, body").animate({ scrollTop: $(document).height() },200);
  })
}





$(document).ready(function(){
  shareClick()
  clickAbout()
})