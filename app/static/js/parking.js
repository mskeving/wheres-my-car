$(document).ready(function() {
    if ($('.new-location-content').length > 0) {
        currentLocationMap();
    } else if ($('.street-cleaning-content').length > 0) {
        carLocationMap();
    }

    $('#change-loc-butt').on('click', function() {
        document.location.href = '/park';
    });

    $('#submit-new-location').on('click', function() {
        // assuming address coming in as NUMBER STREETNAME
        // as in.. before first space is the number and everything after
        // the first space will be the street information
        var address = $('.location-text').text();
        var streetNum = address.substr(0, address.indexOf(' '));
            streetName =  address.substr(address.indexOf(' ')+1);

        if (!Number(streetNum.substr(-1))){
            // if last character isn't a number, get rid of it
            streetNum = streetNum.slice(0, -1);
        }

        $.ajax({
            type: "Post",
            url: '/new-location',
            data: {
                streetNum: streetNum,
                streetName: streetName
            },
            success: function() {
                //document.location.href = '/';
                console.log('success');
            },
            error: function() {
                alert('error submitting address');
            }
        })

    })
});


function carLocationMap() {
    var map = new google.maps.Map(document.getElementById('map-canvas'));
    var marker = new google.maps.Marker();
    var geocoder = new google.maps.Geocoder();
    var address = $('.location-text').text();

    geocoder.geocode({'address': address}, function (results, status) {
        var pos = new google.maps.LatLng(results[0]['geometry'].location.lat(),
                                        results[0]['geometry'].location.lng());
        marker.setOptions({
            map: map,
            position: pos
        });
        map.setOptions({
            center: pos,
            zoom: 17
        });
    });
}

function currentLocationMap() {
    var map = new google.maps.Map(document.getElementById('map-canvas'));
    var marker = new google.maps.Marker();
    var geocoder = new google.maps.Geocoder();

    function displayAddress(address) {
        var streetAddress = address.split(',')[0];
        $('.location-text').text(streetAddress);
    }

    //HTML geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                                            position.coords.longitude);

            marker.setOptions({
                map: map, 
                draggable: true,
                position: pos
            });

            geocoder.geocode({'latLng': pos}, function (results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    if (results[0]) {
                        // results is an array. 0 being most specific postal 
                        // address to 6 referring to United States
                        displayAddress(results[0]['formatted_address']);
                    } else {
                        console.log('no results found');
                    }
                } else {
                    console.log('Geocoder failed due to: ' + status);
                }
            });

            map.setOptions({
                center: pos,
                zoom: 17
            });

        }, function() {
            handleNoGeolocation(true, map);
        });


    } else {
        // browser doesn't support geolocation
        handleNoGeolocation(false, map);
    }

}

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
