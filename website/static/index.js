$(document).ready(function() {
    console.log()
    
    $('.deletebtn').on('click', function(e) {
        var url=$(this).parent().prop('action');
        var li=$(this).closest('li');
        console.log(url)
        $.ajax({
            url:url,
            type:'post',
            contentType:'application/json',
            success: function(response){
                if (response) {
                    li.fadeOut(1000, function(){ // **add this
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








})