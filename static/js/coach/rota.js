$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }

    $.ajax({
        type: 'get',
        url: '/rota_data/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
             counter = 0;
             console.log(data.data,"rota");
             jQuery.each(data.data, function (i, item) {
                 html = `<div class="col-md-3" style="border: 3px solid #043a75b8;width:500px;margin-bottom:10px;">
                        <center>
                                <b style="text-align:center;">${item.start_date}</b><br>
                        </center>`
                     groups = JSON.parse(item.course_detail.course_details);

                    jQuery.each(groups, function (i, value) {
                        if (value.coach1 == null){
                            coach1 = "";
                        }
                        else {
                            coach1 = value.coach1;
                        }

                        if (value.coach2 == null){
                            coach2 = "";
                        }
                        else {
                            coach2 = value.coach2;
                        }

                        html +=  `<ul class="list list-marked">
                                    <li>${item.course_detail.location.location}</li>
                                </ul>
                                <input type="search" placeholder="Assisting Coach 1" class="search" onfocusout="setCoach1('${item.course_detail.id}', '${value.id}', $(this).val())" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="${coach1}"><br>
                                <input type="search" id="search${counter}" class="search" placeholder="Assisting Coach 2" onfocusout="setCoach2('${item.course_detail.id}', '${value.id}', $(this).val())" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="${coach2}"><br>
                                <input type="text" placeholder="Address" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="Address: ${item.course_detail.location.address_line_1}"><br>
                                <input type="text" placeholder="Course Time" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="Course Time: ${value.time}">`

                        counter += 1
                    });
                    html += `</div>`
                           $( ".search" ).autocomplete({
                                source: function (request, response) {
                                    console.log(request.term)
                                    $.ajax({
                                        url: '/populate_coaches/',
                                        data: {
                                          'coach': request.term
                                        },
                                        dataType: 'json',
                                        type: "GET",
                                        contentType: "application/json; charset=utf-8",
                                        success: function (data) {
                                            if (data.coach.length > 0) {
                                                response($.map(data.coach, function (item) {
                                                    return {
                                                        label: item,
                                                        val: item
                                                    };
                                                }))
                                            } else {
                                                response([{ label: 'No results found.', val: -1}]);
                                            }
                                        }
                                    });
                                },
                                select: function (e, u) {
        if (u.item.val == -1) {
            return false;
        }
    }
                            });
                 $('#rota-table').append(html);
             });
        },
        error: function(data) {
            url = "/rota/"
            if(data.status == 401)
            {
                getAccessToken(url)
            }
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
});


$("#rota-filter").change(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }

    if (this.value != "Select"){
        $.ajax({
            type: 'get',
            url: '/rota_data/'+this.value,
            headers: { Authorization: 'Bearer ' + access.access },
            data: {},
            success: function(data) {
                $('#rota-table').empty();
                 console.log(data.data,"rota");
                 jQuery.each(data.data, function (i, item) {
                     html = `<div class="col-md-3" style="border: 3px solid #043a75b8;width:500px;margin-bottom:10px;">
                            <center>
                                    <b style="text-align:center;">${item.start_date}</b><br>
                            </center>`
                         groups = JSON.parse(item.course_detail.course_details);
    
                        jQuery.each(groups, function (i, value) {
                            if (value.coach1 == null){
                                coach1 = "";
                            }
                            else {
                                coach1 = value.coach1;
                            }
    
                            if (value.coach2 == null){
                                coach2 = "";
                            }
                            else {
                                coach2 = value.coach2;
                            }
    
                            html +=  `<ul class="list list-marked">
                                        <li>${item.course_detail.location.location}</li>
                                    </ul>
                                    <input type="search" class="search" placeholder="Assisting Coach 1" onfocusout="setCoach1('${item.course_detail.id}', '${value.id}', $(this).val())" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="${coach1}"><br>
                                    <input type="search" class="search"  placeholder="Assisting Coach 2" onfocusout="setCoach2('${item.course_detail.id}', '${value.id}', $(this).val())" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="${coach2}"><br>
                                    <input type="text" placeholder="Address" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="Address: ${item.course_detail.location.address_line_1}"><br>
                                    <input type="text" placeholder="Course Time" style="background-color:#80808000;border: 1px solid grey; width:250px;" value="Course Time: ${value.time}">`
                        });
                        html += `</div>`
                        $( ".search" ).autocomplete({
                                    source: function (request, response) {
                                        console.log(request.term)
                                        $.ajax({
                                            url: '/populate_coaches/',
                                            data: {
                                              'coach': request.term
                                            },
                                            dataType: 'json',
                                            type: "GET",
                                            contentType: "application/json; charset=utf-8",
                                            success: function (data) {
                                                if (data.coach.length > 0) {
                                                    response($.map(data.coach, function (item) {
                                                        return {
                                                            label: item,
                                                            val: item
                                                        };
                                                    }))
                                                } else {
                                                    response([{ label: 'No results found.', val: -1}]);
                                                }
                                            }
                                        });
                                    },
                                    select: function (e, u) {
            if (u.item.val == -1) {
                return false;
            }
        }
                                });
                     $('#rota-table').append(html);
                 });
            },
            error: function(data) {
                url = "/rota/"
                if(data.status == 401)
                {
                    getAccessToken(url)
                }
                console.log(data);
            },
        });
    }


});

function setCoach1(id, gid, value){
    console.log(id, gid, value);
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }

    $.ajax({
        type: 'post',
        url: '/rota_data/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {
            'course_id': id,
            'course_group_id': gid,
            'coach1': value,
        },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
            url = "/rota/"
            if(data.status == 401)
            {
                getAccessToken(url)
            }
            console.log(data);
        },
    });
}

function setCoach2(id, gid, value){
    console.log(id, gid, value);
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }

    $.ajax({
        type: 'post',
        url: '/rota_data/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {
            'course_id': id,
            'course_group_id': gid,
            'coach2': value,
        },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
            url = "/rota/"
            if(data.status == 401)
            {
                getAccessToken(url)
            }
            console.log(data);
        },
    });
}

