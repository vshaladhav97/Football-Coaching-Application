var counter = 0;
var student_id = [];
var total_fees = 0;
var week_tables_fees = 0;
var price_matrix_id;
var perWeekbooking_MainObj = sessionStorage.getItem("perWeekbookingMainObj");
console.log(perWeekbookingMainObj);
var perWeekbookingMainObj = JSON.parse(perWeekbooking_MainObj);
var course = localStorage.getItem("course_type_id");
var course_detail_id = localStorage.getItem("course_detail_id")
var course_type_name = localStorage.getItem("course_type_name");
var customer_id;
var description;

if (localStorage.getItem("customer_id") !== null) {
  customer_id = localStorage.getItem("customer_id");
} else {
  customer_id = localStorage.getItem("customers_new_id");
}

if (perWeekbookingMainObj != null) {
  perWeekbookingMainObj.customer = parseInt(
    localStorage.getItem("customer_id")
  );
}
// console.log(perWeekbookingMainObj);

$(".preschool").hide();
$(".week1").hide();
$(".week2").hide();
$(".summary__container").hide();
$("#discount_info_div").hide();


// to filter student who has already done payments.
var payment_done_student_id = [];
$(document).ready(function () {
  $.ajax({
    type: "get",
    url: "/student_with_payment_done/" + localStorage.getItem("customer_id"),
    data: {},
    success: function (data) {
      console.log(data);
      data.forEach((element) => {
        console.log(element.nursery_and_weekly_student_order_details.student);
        payment_done_student_id.push(
          element.nursery_and_weekly_student_order_details.student
        );
        localStorage.setItem(
          "payment_student",
          JSON.stringify(payment_done_student_id)
        );
      });
    },
  });
});


course_type_id = localStorage.getItem("course_type_id")

$(document).ready(function () {
  sessionStorage.getItem("perWeekbookingMainObj", null);

  // var customer_id = 53
  if (localStorage.getItem("course_type_name") == "Nursery") {
    $(".preschool").show();

    if (customer_id != null) {
      $.ajax({
        type: "get",
        url: "/student_with_course_type/" + customer_id + '/' +course_type_id,
        // headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function (data) {
          // to filter out already done payment.
          if (payment_done_student_id.length != 0) {
            data = data.filter((val) => !payment_done_student_id.includes(val.id));
          }

          jQuery.each(data, function (i, item) {
          
            counter = counter + 1;

            student_id.push(item.id);

            html = `<td>child ${counter}</td>`;

            $("#children_count").append(html);

            html = `<td>${item.firstname}</td>`;
            $("#children_name").append(html);
          });
          
          html = `<td>Total</td>`;
          $("#children_name").append(html);
          priceMatrix();
          $("#description").text(
            "Buy this " +
              localStorage.getItem("course_type_name") +
              " course for " +
              localStorage.getItem("counter_for_children") +
              " children"
          );

          // $("#total_fees").append(html);
       
          localStorage.setItem("student_id", JSON.stringify(student_id));
        }, // success function ends here.
      }); //ajax ends here
      
    } else {
      // $.ajax({
      //   type: "get",
      //   url: "/recent_students/" + 3,
      //   // headers: { Authorization: 'Bearer ' + access.access },
      //   data: {},
      //   success: function (data) {
      //     jQuery.each(data.data, function (i, item) {
      //       counter = counter + 1;
      //       var fees = 25;
      //       total_fees = total_fees + fees;
      //       html = `<td>child ${counter}</td>`;
      //       $("#children_count").append(html);
      //       html = `<td>${item.first_name}</td>`;
      //       $("#children_name").append(html);
      //       html = `<td>£${fees}</td>`;
      //       $("#children_fees").append(html);
      //     });
      //     html = `<td>Total</td>`;
      //     $("#children_name").append(html);
      //     html = `<td class="total">£${total_fees}</td>`;
      //     $("#children_fees").append(html);
      //     // $("#total_fees").append(html);
      //   }, // success function ends here.
      // }); //ajax ends here
    }
  } else if (
    localStorage.getItem("course_type_name") == "Evening Development"
  ) {
    $(".preschool").show();
    var child_id = JSON.parse(localStorage.getItem("student_id"));
    console.log(student_id);

    if (customer_id != null) {
      $.ajax({
        type: "get",
        url: "/student_details_by_customer/" + customer_id,
        // headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function (data) {
          jQuery.each(data.data, function (i, item) {
            for (j = 0; j < child_id.length; j++) {
              if (item.id == child_id[j]) {
                counter = counter + 1;

                student_id.push(item.id);

                html = `<td>child ${counter}</td>`;

                $("#children_count").append(html);

                html = `<td class="${course_type_name}">${item.first_name}</td>`;
                $("#children_name").append(html);
              }
            }
          });
          html = `<td class="${course_type_name}">Total</td>`;
          $("#children_name").append(html);
          priceMatrixEveDev();
          $("#description").text(
            "Buy this " +
              localStorage.getItem("course_type_name") +
              " course for " +
              child_id.length +
              " children"
          );

          // $("#total_fees").append(html);
        }, // success function ends here.
      }); //ajax ends here
    } else {
      $(".week1").show();
      $(".week2").show();
      $(".summary__container").show();
      $("#discount_info_div").show();
      prepareDynamicOrderSummary(perWeekbookingMainObj);

      $("#description").text(
        "Buy this " +
          localStorage.getItem("course_type_name") +
          " course for " +
          perWeekbookingMainObj.perWeekArr[0].childArr.length +
          " children"
      );
    }
  }
}); //document.ready ends here
var student_id= []
function GoBackFromOrderSummary() {
  localStorage.removeItem('myMap');
  // localStorage.setItem("student_id", JSON.stringify(student_id));
  localStorage.removeItem('student_id')
  var user_id = localStorage.getItem("user_id");

  if (localStorage.getItem("course_type_name") == "Nursery") {
    if (user_id != null) {
      window.location.href = "/course_edit_by_venue/";
    } else {
      window.location.href = "/check_for_member/";
    }
  } else if (
    localStorage.getItem("course_type_name") == "Evening Development"
  ) {
    if (user_id != null) {
      window.location.href = "/course_edit_by_venue/";
    } else {
      window.location.href = "/check_for_member/";
    }
  } else {
    if (user_id != null) {
      window.location.href = "/week_booking/";
    } else {
      window.location.href = "/check_for_member/";
    }
  }
}

function BookCourse() {
  if ((localStorage.getItem("course_type_name") == "Nursery") || (localStorage.getItem("course_type_name") == "Evening Development")){
    localStorage.removeItem('myMap');
    var total_payment = total_fees;
    if (total_payment === 0) {
      $(
        ".order_summary_modal_popup, #changePasswordModal, #comfirm__order, #exampleModal"
      ).modal("hide");
      $("body").removeClass("modal-open");
      $(".modal-backdrop").remove();
      toastr.warning("Total Amount cannot be 0");
      return false;
    }
    var customer_id = parseInt(localStorage.getItem("customer_id"));
    description = $("#description").text();
    var student_order = JSON.parse(localStorage.getItem("student_id"));
    // console.log(student_order)
    // for(j=0; j<student_data.length; j++){
      var order_data = {
        // day_wise_week_details: 1,
        customer_id: customer_id,
        description: description,
        student_order : student_order,
        amount: total_payment,
        order_details: {
          event_week: [],
          customer: customer_id,
          total_cost: total_payment,
          price_matrix: price_matrix_id,
          discounted_amount: 0,
        },
      };
      console.log(order_data)

    $.ajax({
      type: "POST",
      url: "/save_order_details/",
      data: JSON.stringify(order_data),
      contentType: "application/json",
      dataType: "json",
      success: add_success,
      error: add_error,
    });
    // }
    


  } 
  
  
  else {
    perWeekbookingMainObj.description = $("#description").text();
    console.log(perWeekbookingMainObj);

    $.ajax({
      type: "POST",
      url: "/save_order_details_for_other_category/",
      data: JSON.stringify(perWeekbookingMainObj),
      contentType: "application/json",
      dataType: "json",
      success: add_success,
      error: add_error,
    });
  }
}

// function add_success(data) {
//   //Code here is been removed by conflict change the value from true
//   if (true) {
//     $(
//       ".order_summary_modal_popup, #changePasswordModal, #comfirm__order, #exampleModal"
//     ).modal("hide");
//     $("body").removeClass("modal-open");
//     $(".modal-backdrop").remove();
//     window.open(data.data);
//   } else {
//     $.ajax({
//       type: "POST",
//       url: "/save_order_details_for_other_category/",
//       data: JSON.stringify(perWeekbookingMainObj),
//       contentType: "application/json",
//       dataType: "json",
//       success: add_success,
//       error: add_error,
//     });
//   }
// }

function add_success(data) {
  $(
    ".order_summary_modal_popup, #changePasswordModal, #comfirm__order, #exampleModal"
  ).modal("hide");
  $("body").removeClass("modal-open");
  $(".modal-backdrop").remove();
  window.open(data.data);
  // console.log(data);
}

function add_error() {
  toastr.error("Could not make customer order!");
  return false;
}

/*
function processFinalPayment(perWeekbookingMainObj){
    $.ajax({
        type: "POST",
        url: "/save_order_details",
        data: JSON.stringify(perWeekbookingMainObj),
        contentType: "application/json",
        dataType: "json",
        success: function (data) {
        console.log(data);
          if (data.url) {
            window.open(data.url);
          }
        },
        error: function (data) {
          console.log(error);
        },
      });
  }
}*/

function prepareDynamicOrderSummary(perWeekbookingMainObj) {
  let orderSummaryEle;
  orderSummaryEle = $(".order-summary-parent").empty();
  if (perWeekbookingMainObj) {
    var perWeekArray = perWeekbookingMainObj.perWeekArr;
    $.each(perWeekArray, function (index, value) {
      orderSummaryEle.append(
        '<div class="col-md-12 week_' +
          value.weekNumber +
          '">' +
          '<div class="text-center order_summary_header">' +
          "<h4>Week " +
          value.weekNumber +
          "</h4>" +
          "<h3>" +
          value.weekDisplayTxt +
          "</h3>" +
          "</div></div>"
      );

      orderSummaryEle.append(
        '<div id="summary__containers_week_' +
          value.weekNumber +
          '" class="summary__containers_week_' +
          value.weekNumber +
          '">' +
          '<div id="summary__container_' +
          value.weekNumber +
          '" class="summary__container_' +
          value.weekNumber +
          '">'
      );

      var childArray = value.childArr;
      var allChildNameList = [];
      var allChildAmounts = [];
      $('<table class="table tableWeek_' + value.weekNumber + '">').appendTo(
        ".summary__container_" + value.weekNumber + ""
      );
      $.each(childArray, function (index, childValue) {
        index++;
        allChildNameList.push(
          "<td>" + childValue.number_of_days_pass + " days</td>"
        );
        if (childArray.length == index) {
          allChildNameList.push("<td></td>");
          allChildNameList.push("<td>Saved</td>");
        }
      });
      $(
        `<tr id="children__name" class="${localStorage.getItem(
          "course_type_name"
        )}">`
      )
        .append(allChildNameList.join(""))
        .appendTo(".tableWeek_" + value.weekNumber + "");

      $.each(childArray, function (index, amountValue) {
        index++;
        allChildAmounts.push("<td>£ " + amountValue.cost + "</td>");
        if (childArray.length == index) {
          allChildAmounts.push(
            '<td class="total">£ ' +
              `${value.totalAmountPerWeek ? value.totalAmountPerWeek : 0}` +
              "</td>"
          );
          allChildAmounts.push(
            '<td class="saved">£ ' +
              `${value.totalDiscountPerWeek ? value.totalDiscountPerWeek : 0}` +
              "</td>"
          );
        }
      });

      $('<tr id="children__fees">')
        .append(allChildAmounts.join(""))
        .appendTo(".tableWeek_" + value.weekNumber + "");
    });

    $("#final_value").text("£ " + perWeekbookingMainObj.total_cost);
    $(".total_values").text("£ " + perWeekbookingMainObj.total_cost);

    if (perWeekbookingMainObj.discounted_amount <= 0) {
      $(".you_qualify").hide();
      $(".payNow").hide();
    } else {
      $(".you_qualify").show();
      $(".payNow").show();
    }
    if (perWeekbookingMainObj.total_cost <= 0) {
      $(".payNow").hide();
    } else {
      $(".payNow").show();
    }
  } else {
    $(".you_qualify").hide();
  }
}

// Price Matrix

function priceMatrix() {
  var no_of_weeks_nursery = localStorage.getItem('no_of_weeks')
  $.ajax({
    type: "get",
    url: "/price_matrix/" + course_detail_id,
    data: {},
    success: function (data) {
      price_matrix_id = data.data[0].id;
      for (let i = 0; i < counter; i++) {
        let html = `
                    <td>£${data.data[0].single_day * no_of_weeks_nursery}</td>
                    `;
        $("#children_fees").append(html);
        total_fees = total_fees + data.data[0].single_day*no_of_weeks_nursery;
      }
      html = `<td class="total">£${total_fees}</td>`;
      $("#children_fees").append(html);

      $("#final_value").text("£" + total_fees);
      $(".total_values").text(total_fees);
    },
  }); //ajax
}

function priceMatrixEveDev() {
  var no_of_weeks = localStorage.getItem('no_of_weeks')
  $.ajax({
    type: "get",
    url: "/price_matrix/" + course_detail_id,
    data: {},
    success: function (data) {
      price_matrix_id = data.data[0].id;
      for (let i = 0; i < counter; i++) {
        let html = `
                    <td>£${data.data[0].single_day * no_of_weeks}</td>
                    `;
        $("#children_fees").append(html);
        total_fees = total_fees + data.data[0].single_day*no_of_weeks;
      }
      html = `<td class="total">£${total_fees}</td>`;
      $("#children_fees").append(html);

      $("#final_value").text("£" + total_fees);
      $(".total_values").text(total_fees);
    },
  }); //ajax
}
