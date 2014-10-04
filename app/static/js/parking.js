$(document).ready(function() {
    function initialize() {
        var myLatlng = new google.maps.LatLng(37.736248,-122.448935);
        var mapOptions = {
            center: myLatlng,
            zoom: 17
        };
        var map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            map: map
        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);

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
