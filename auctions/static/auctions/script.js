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
        let wishlistInp = $('#wishlistInp').val();
        $('.e_msg').text('success !');
        $('.e_msg').show();
    })

    $('#removeWatchlistBtn').on('click',function (e) {
        e.preventDefault();
        $('.e_msg').text('success !');
        $('.e_msg').show();
    })
    
    $('#commentForm').on('submit',function (e) {
        e.preventDefault();
        $('.e_msg').text('success !');
        $('.e_msg').show();
    })
})