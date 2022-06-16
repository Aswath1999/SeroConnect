$(document).ready(function() {
    console.log()
    
    $('#deletebtn').on('click', function(e) {
        var url=$('.deleteform').prop('action');
        var li=$(this).closest('li');
        console.log(url)
        $.ajax({
            url:url,
            type:'post',
            contentType:'application/json',
            success: function(response){
                console.log('success')
                if (response) {
                    li.fadeOut(1000, function(){ // **add this
                        $(this).remove();
                    });
                }

            }
        })
        e.preventDefault();
    })








})