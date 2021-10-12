$("#checkbox-error-msg").hide();
var counter = 0;
$(document).ready(function (){

    course = localStorage.getItem('course')
    $.ajax({
        type: 'get',
        url: '/edit_booking/'+course,
        // headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            $('#edit-booking').empty();

            html = `BOOKINGS - ${data.data.location}`
            $(`#booking_header`).append(html);

            html = `<img src="${data.data.logo}" style="height: 230px; width: 100%;" ></img>`
            $('#first-div-first-child').append(html)

            html = `
            <b style="text-align:center;">${data.data.course_type}</b><br>
        `
            $('#first-div-second-child').append(html)

            html = `<span class="group-contents">
            <span class="group-style-1">
                <span style="display: flex; margin-bottom: 10px;">
                    <label>Start Date: ${data.data.start_date_with_day}</label>
                    <label "></label>
                </span>
                
            <span style="display: flex; margin-bottom: 10px;">
                <label>Duration: ${data.data.no_of_weeks} Weeks</label>
                
            </span>
            
            <span style="display: flex; margin-bottom: 10px;">
                <label>Weekly Cost: £ ${data.data.default_course_rate}</label>

            </span>
            </span>
            </span>`
            $('#second-div-first-child').append(html)

            
        jQuery.each(data.data.course_group, function (i, item) {
            counter = counter + 1
            
            html = `<div>
            <span class="course-group">
            <span class="ages">
            <table style="width:100%">
            <tr class="group-style">
            <td style="width: 238px; text-align:center;"><span style="font-weight: bold;">Group ${counter}</span> - ${item.age.age}</td>

            </tr>
            <hr>
            </table>
            </span>
            </span>
            </div>
            `
            $('#second-div-second-child').append(html)         
            });

   
            html = `<span class="time-contents">
            <span class="time-content-1">
            <span><label><strong>Preston -</strong>${data.data.location}</label>
            </span>

            <span>
            <label style="margin-top:20px;">Every <span style="color:red;">${data.data.day_filter}</span style="color:red;"></label>
            
          </span>            
            
            
            </span>
            </span>`

            $('#third-div-first-child').append(html) 


                
            jQuery.each(data.data.course_group, function (i, item) {
            
                // counter = counter + 1;
            html = `<div>
                <span class="times" >
                <table style="width: 100%; text-align: center;">
                <tr class="time-content">
                <td >${item.start_time} to ${item.end_time} <select name="" id="dropdowns" class="dropdwn">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select></td>
                </tr>
                <hr>
                </table>
                </span>
                </div>
                    `
                $('#third-div-second-child').append(html)        
            });


            html = `
            Total Selected 

            `+counter

            $('#third-div-third-child').append(html) 

        

        } // success function ends here.

        });//ajax ends here

        }); //document.ready ends here

//to select only one checkbox at a time
$('input.chk').on('change', function() {
    $("#checkbox-error-msg").hide();
    $('input.chk').not(this).prop('checked', false);  
});

function getbookinglist(){
    // localStorage.setItem('course',id)
    if($("#new-customer-checkbox").prop('checked') == true){
        //do something
        
        window.location.href = "/registration_part1/"
    }
    else if($("#existing-customer-checkbox").prop('checked') == true){
        
        window.location.href = "/parents/"
    }
    else{
        $("#checkbox-error-msg").show();
        // alert("Please select the checkbox to click on next button.");
        // var modal = document.getElementById("myModal");
        // var span = document.getElementsByClassName("close")[0];
        // modal.style.display = "block";
        // span.onclick = function() {
        //     modal.style.display = "none";
        // }
        // window.onclick = function(event) {
        //     if (event.target == modal) {
        //       modal.style.display = "none";
        //     }
        // }
        // $('#myModal').show();
        // var favorite = [];
        // $.each($("input[name='sport']:checked"), function() {
        // favorite.push($(this).val());
        // });
        // $('#myModal').modal('show').on('shown.bs.modal', function() {
        // $("#checkid").html("My favourite sports are: " + favorite.join(", "));
        // });
    }
    
}
