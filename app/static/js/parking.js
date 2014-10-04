$(document).ready(function() {
    $('#change-loc-butt').on('click', function() {
        document.location.href = '/park';
    });

    $('#submit-new-location').on('click', function() {
        var streetNum = '805',
            streetName =  'FOERSTER ST';

        $.ajax({
            type: "Post",
            url: '/new-location',
            data: {
                streetNum: streetNum,
                streetName: streetName
            },
            success: function() {
                document.location.href = '/';
                console.log('success');
            },
            error: function() {
                alert('error submitting address');
            }
        })

    })
});

function displayStreetCleaning() {
    return;
}
