$(document).ready(function() {
    function initializeMap() {
        var mapElm = document.getElementById('map-canvas');
        var mapOptions = {
            zoom: 17
        };
        var map = new google.maps.Map(mapElm, mapOptions);

        //HTML geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                                                position.coords.longitude);
                var marker = new google.maps.Marker({
                    map: map, 
                    draggable: true,
                    position: pos
                });

                map.setCenter(pos);
            }, function() {
                handleNoGeolocation(true, map);
            });

        } else {
            // browser doesn't support geolocation
            handleNoGeolocation(false, map);
        }

    }

    google.maps.event.addDomListener(window, 'load', initializeMap);

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

function handleNoGeolocation(errorFlag, map) {
    if (errorFlag) {
        var content = 'Error: Geolocation failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }

    var options = {
        map: map,
        position: new google.maps.LatLng(60,105),
        content: content
    };

    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

function detectBrowser() {
    console.log('ys');
    var useragent = navigator.userAgent;
    var mapdiv = document.getElementById("map-canvas");
  
    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
        mapdiv.style.width = '100%';
        mapdiv.style.height = '100%';
    } else {
        mapdiv.style.width = '600px';
        mapdiv.style.height = '800px';
    }
}
