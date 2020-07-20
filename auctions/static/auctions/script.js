$(document).ready(function () {

    setInterval(function () {
        $('.e_msg').hide();
    }, 5000);

    $('.menu').on('click',function () {
        $('.navb').show();
    })

    $('.toggle').on('click',function () {
        $('.navb').hide();
    })
    
    $('#addWatchlistBtn').on('click',function (e) {
        e.preventDefault();
        let id = $('#wishlistInp').val();
        $.ajax({
            url:'',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name~="csrfmiddlewaretoken"]').val(),
                addLid:id
            },
            success: function (data) {
                if (data=='Added to watchlist !'){
                    // $(addWatchlistBtn).hide();
                    // $(removeWatchlistBtn).show();
                    $('.e_msg').text(data);
                    $('.e_msg').show();
                    window.location = 'listing?q='+id
                }
            }
        })
    })

    $('#removeWatchlistBtn').on('click',function (e) {
        e.preventDefault();
        var r = confirm('Do you really want to remove this item from your watchlist?');
        if (r == true){
            let id = $('#wishlistInp').val();
            $.ajax({
                url:'',
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: $('input[name~="csrfmiddlewaretoken"]').val(),
                    reLid:id
                },
                success: function (data) {
                    if (data=='Removed from watchlist !'){
                        // $(removeWatchlistBtn).hide();
                        // $(addWatchlistBtn).show();
                        $('.e_msg').text(data);
                        $('.e_msg').show();
                        window.location = 'listing?q='+id
                    }else{
                        $('.e_msg').text(data);
                        $('.e_msg').show();
                    }
                }
            })
        }
    })

    $("#commentForm").on('submit', function (e) {
        e.preventDefault();
        let id = $('#wishlistInp').val();
        $.ajax({
            url: '',
            method: 'POST',
            data: $("#commentForm").serialize(),
            success: function (data) {
                if (data == 'comment added successfully') {
                    window.location = 'listing?q='+id
                }
            }
        })
    })
})