var counter = 0;
var total_fees = 0;
var startDateOfCourse=null;
var endDateOfCourse=null;
var maxWeekNumber=null;
var perWeekbookingMainObj={};
var startWeekBackDayCount = 0;
var endWeekForwardDayCount=0;
var eventTypeId=null;
var course_type_name = localStorage.getItem("course_type_name")
var customer_id
// console.log(course_type_name);
/// $("#summary_container").hide();
$(document).ready(function () {
    var course = localStorage.getItem("course_type_id");
    var location_id = localStorage.getItem("location_id");
    var no_of_childs = localStorage.getItem("no_of_childs");
    
    if (localStorage.getItem("customer_id") == null){
      customer_id = localStorage.getItem("customers_new_id");
    }
    else{
      customer_id = localStorage.getItem("customer_id");
    }
    
    let childDateSet=callStudentDetailsByCustomer(customer_id);
    callBookingByCourseTypeData(location_id,course,childDateSet);
    getPriceMatrixForCourse(course);
    getEventDateDiff();
}); //document.ready ends here


function getEventDateDiff(){
    var strDate = new Date(startDateOfCourse);
    var endDate = new Date(endDateOfCourse);
    var startWeekOfCourse=getClosestMonday(startDateOfCourse);
    var endWeekOfCourse=getCommingSunday(endDateOfCourse);

    startWeekBackDayCount = getStartDates(startWeekOfCourse, strDate);
    endWeekForwardDayCount = getEndDates(endDate, endWeekOfCourse);
    // console.log('endDateOfCourse---',startDateOfCourse,'===endWeekForwardDayCount--'
    // ,endWeekForwardDayCount,'--startWeekBackDayCount==',startWeekBackDayCount);
}

var getStartDates = function(startDate, endDate) {
    var dates = [],
        currentDate = startDate,
        addDays = function(days) {
          var date = new Date(this.valueOf());
          date.setDate(date.getDate() + days);
          return date;
        };
    while (currentDate < endDate) {
      dates.push(currentDate);
      currentDate = addDays.call(currentDate, 1);
    }
    return dates.length;
  };

  var getEndDates = function(startDate, endDate) {
    var dates = [],
        currentDate = startDate,
        addDays = function(days) {
          var date = new Date(this.valueOf());
          date.setDate(date.getDate() + days);
          return date;
        };
    while (currentDate < endDate) {
      dates.push(currentDate);
      currentDate = addDays.call(currentDate, 1);
    }
    return dates.length;
  };




function callBookingByCourseTypeData(location_id,course,childDateSet){
    $.ajax({
        type: "get",
        async:false,
        url: "/booking_by_course_type_data_for_others/" + location_id + "/" + course,
        // headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function (data) {
            html = `
                <div>${data.data[0].start_date}</div>
                <div>Select a child from each name dropbox</div>
                `;
      $("#date_with_detail").append(html);
      startDateOfCourse = data.data[0].start_date;
      console.log("startDateOfCourse ==" + startDateOfCourse);
      endDateOfCourse = data.data[0].end_date;
      console.log("endDateOfCourse ==" + endDateOfCourse);
      maxWeekNumber = data.data[0].no_of_weeks;
      console.log("maxWeekNumber ==" + maxWeekNumber);
      eventTypeId=data.data[0].event_type;
      calculateDateAndWeekToRenderView(childDateSet, false);
    }, // success function ends here.
  }); //ajax ends here
}

//Get Price matrix details for course.
function getPriceMatrixForCourse(course){
    $.ajax({
        type: "get",
        async:false,
        url: "/price_matrix/" + course,
        data: {},
        success: function (data) {
          $('#singleDay').val(data.data[0].single_day);
          $('#twoDays').val(data.data[0].two_days);
          $('#threeDays').val(data.data[0].three_days);
          $('#fourDays').val(data.data[0].four_days);
          $('#fiveDays').val(data.data[0].five_days);
          $('#single_day_price').text(data.data[0].single_day);
          $('#two_day_price').text(data.data[0].two_days);
          $('#three_day_price').text(data.data[0].three_days);
          $('#four_day_price').text(data.data[0].four_days);
          $('#five_day_price').text(data.data[0].five_days);
          perWeekbookingMainObj.price_matrix_id=(data.data[0].id);
        },
    }); //ajax ends here

}

function callStudentDetailsByCustomer(customer_id) {
  let responseChildSet = null;
  $.ajax({
    type: "get",
    async: false,
    url: "/student_details_by_customer/" + customer_id,
    // headers: { Authorization: 'Bearer ' + access.access },
    data: {},
    success: function (data) {
      responseChildSet = data;
    }, // success function ends here.
  }); //ajax ends here
  return responseChildSet;
}

