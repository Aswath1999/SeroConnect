$(document).ready(function() {
    console.log()   

    $('.deletebtn').on('click', function(e) {
        var url=$(this).parent().prop('action');
        var section=$(this).closest('section');
        console.log(url)
        $.ajax({
            url:url,
            type:'post',
            contentType:'application/json',
            success: function(response){
                if (response) {
                    section.fadeOut(1000, function(){ // **add this
                        $(this).remove();
                        console.log(response)
                    });
                }
                else{
                    console.log('failure')
                }

            }
        })
        e.preventDefault();
    })

    $(function() {
        $("#btn2").click(function() {
          $(this).closest("form").attr('action', '/anonymous');
        });
      });

    $(function() {
        $("#btn1").click(function() {
          $(this).closest("form").attr('action', '/forum/post');
        });
    });

 
    // Delete comments ajax
    $('.deletecomment').on('click', function(e) {
        var url=$(this).parent().prop('action');
        var div=$(this).closest('div');
        console.log(url)
        $.ajax({
            url:url,
            type:'post',
            contentType:'application/json',
            success: function(response){
                if (response) {
                    div.fadeOut(1000, function(){ // **add this
                        $(this).remove();
                        console.log(response)
                    });
                }
                else{
                    console.log('failure')
                }

            }
        })
        e.preventDefault();
    })


    $('.comments').css('display', 'none')
        // comment display ajax request
    $('.cmt').on('click', function(e) {
        $(this).children('div').show()
    })

    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
    

})