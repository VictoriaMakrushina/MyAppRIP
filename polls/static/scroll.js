var inProgress = false;
var startFrom = 4;
$(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height()- 100 && !inProgress) {
        $.ajax({
            url: '/load/',
            method: 'get',
            data: {"start": startFrom},
            beforeSend: function () {
                inProgress = true;
            }
        }).done(function (data) {
            console.log(data.length);
            console.log(data);
            if (data.length > 0) {

                for(let i = 0; i < data.length; i++){
                    let inf = data[i].fields;
                    let $cour = $('#course_id-6').clone();
                    $cour.attr('id', 'course_id-'+data[i].id);
                    $cour.find('#name').text(data[i].name);
                    $cour.find('#name').attr('href', '/course/'+data[i].id);
                    $cour.find('#imgid').text(data[i].description);
                    $cour.find('#imgu').attr('src', data[i].avatar);
                    $cour.find('#imgCos').text(data[i].cost);

                    $('#thread').append($cour);
                    console.log($('#thread'));
                }

                inProgress = false;
                startFrom += 4;
            }
        });
    }
});