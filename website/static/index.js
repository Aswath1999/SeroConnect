$(document).ready(function() {
    console.log()   
// Ajax for deleting posts
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
                    section.fadeOut(500, function(){ // **add this
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
// Ajax for creating comments
$('#createcomment').on('click', function(e) {
    let url=$('.createcommentform').prop('action');
    $.ajax({
        url:url,
        type:'post',
        dataType: "json",
        data:JSON.stringify({
            data: $('#commenttext').val()
        }),
        contentType: "application/json",
        success: function(response){
            if(response){
                location.reload();
            }
        },
        error: function(e) {
            console.log(e);
        },
    })
    e.preventDefault();
})

    // submits form info to the link based on button click.
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

 
    // Ajax request for deleing comments
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
                    div.fadeOut(500, function(){ // **add this
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
// Ajax for deleting video
$('.deletevideo').on('click', function(e) {
    var url=$(this).parent().prop('action');
    var section=$(this).closest('section');
    console.log(url)
    $.ajax({
        url:url,
        type:'post',
        contentType:'application/json',
        success: function(response){
            if (response) {
                section.fadeOut(500, function(){ // **add this
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
// prevents submitting the form twice on reload
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
    

})
