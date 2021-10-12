var address
$(document).ready(function () {
  
  if (sessionStorage.getItem("whichScope") == "parent") {
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf("/") + 1);
    $.ajax({
      type: "get",
      url: "/customers/" + id,
      data: {},
      success: function (data) {
        $("#email").focus();
        $("#email").val(data.data.email);
        $("#first_name").focus();
        $("#first_name").val(data.data.first_name);
        $("#last_name").focus();
        $("#last_name").val(data.data.last_name);
        $("#mobile").focus();
        $("#mobile").val(data.data.mobile);
        $("#landline").focus();
        $("#landline").val(data.data.landline);
        $("#town").focus();
        $("#town").val(data.data.town);
        $("#address").focus();
        $("#address").val(data.data.address);
        $("#postal_code").focus();
        $("#postal_code").val(data.data.postal_code);
      },
      error: function (data) {
        console.log(data);
      },
    });
  } else {

    
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf("/") + 1);
    $.ajax({
      type: "get",
      url: "/student_data/" + id,
      data: {},
      success: function (data) {
        $("#first_name_child").focus();
        $("#first_name_child").val(data[0].first_name);
        $("#last_name_child").focus();
        $("#last_name_child").val(data[0].last_name);
        // if (data[0].school_name) {
        //   $("#school_name").focus();
        //   $("#school_name").val(data[0].school_name);
        // }
        // if (data[0].address_details_id) {
          
        //   // $.ajax({
        //   //   type: "get",
        //   //   url: "/address_details_for_prepolation/",
        //   //   data: {},
        //   //   success: function (address_details) {
              
        //   //     var i;
        //   //     for(i=0; i<address_details.length; i++){
        //   //       // if (address_details[i].id == data[0].address_details_id){
                 
        //   //       // }
        //   //       // else{
        //   //       //   html = ` <option value="${address_details[i].id}" >${address_details[i].town}</option>`
        //   //       // }
        //   //       html = `
        //   //       <option value="${address_details[i].id}" >${address_details[i].town}</option>`
        //   //       $("#address_dropdown").append(html);
        //   //     }
        //   //     // $("#address_dropdown").value(2);
                
        //   //   },
        //   //   error: function (address_details) {
        //   //     console.log(address_details);
        //   //   },
            
        //   // });
          
        //   // $("#address_dropdown option[value=1]").attr("selected", true);              
        //   // $('#address_dropdown').val(data[0].address_details_id);
        //   // $('#address_dropdown option[value="1"]').attr("selected",true);
          

    
        //   // $("#address_dropdown").focus();
        //   // $('#address_dropdown option[value="1"]').attr("selected",true);
        //   // $('#address_dropdown option[value=1]').attr('selected','selected');
        //   // $("#address_dropdown").val(data[0].address_details_id);
        //   // $("div#selection address_dropdown.address_dropdown select").each(function(){
        //   //   if($(this).val()==1){ // EDITED THIS LINE
        //   //       $(this).attr("selected","selected");    
        //   //   }
        // // });


        // }
        // $("#address_dropdown").focus();
      

        // $("#customer").focus();
        // $("#customer").val(data[0].customer);
        $("#birthdate").focus();
        $("#birthdate").val(data[0].birthdate);
        $("#medical_issue").focus();
        $("#medical_issue").val(data[0].medical_issue);
      },
      error: function (data) {
        console.log(data);
      },
    });
  }
});

function IsEmail(email) {
  var regex =
    /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  if (!regex.test(email)) {
    return false;
  } else {
    return true;
  }
}

//function isValidPostcode(p) {
//    var postcodeRegEx = /[A-Z]{1,2}[0-9]{1,2} ?[0-9][A-Z]{2}/i;
//    return postcodeRegEx.test(p);
//}

function checkForm(form) {
  if (IsEmail($("#email").val()) == false) {
    $("#email")
      .parent()
      .append('<span class="error">Please enter email.</span>')
      .addClass("has-error");
    return false;
  }
  if ($("#first_name").val() == "") {
    $("#first_name")
      .parent()
      .append('<span class="error">Please enter first name.</span>')
      .addClass("has-error");
    return false;
  }

  if ($("#last_name").val() == "") {
    $("#last_name")
      .parent()
      .append('<span class="error">Please enter last name.</span>')
      .addClass("has-error");
    return false;
  }

  if ($("#mobile").val() == "") {
    $("#mobile")
      .parent()
      .append('<span class="error">Please enter mobile.</span>')
      .addClass("has-error");
    return false;
  }

  if ($("#address").val() == "") {
    $("#address")
      .parent()
      .append('<span class="error">Please enter address.</span>')
      .addClass("has-error");
    return false;
  }

  if ($("#postal_code").val() == "") {
    $("#postal_code")
      .parent()
      .append('<span class="error">Please enter postal code.</span>')
      .addClass("has-error");
    return false;
  }
}

$("#first_name,#last_name").on("keypress", function (event) {
  var regex = new RegExp("^[a-zA-Z \b]+$");
  var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
  if (!regex.test(key)) {
    event.preventDefault();
    return false;
  }
});

$("#mobile,#landline").on("keypress keyup blur", function (event) {
  $(this).val(
    $(this)
      .val()
      .replace(/[^\d].+/, "")
  );
  if (event.which < 48 || event.which > 57) {
    event.preventDefault();
  }
});

$("#myModal").on("hidden.bs.modal", function () {
  location.reload();
});

$(document).on("submit", "#user-edit", function (e) {
  if (sessionStorage.getItem("whichScope") == "parent") {
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf("/") + 1);

    validation = checkForm();
    if (validation == false) {
      return false;
    }
    let formData = new FormData($("#user-edit")[0]);
    $.ajax({
      url: "/customers/" + id,
      method: "PUT",
      enctype: "multipart/form-data",
      data: formData,
      contentType: false,
      processData: false,
      async: false,
      success: function (data) {
        window.location.href = "/parents/";
      },
      error: function (data) {
        console.log(data);
      },
    });
  }
});

$(document).on("submit", "#user-edit_child", function (e) {

    if (sessionStorage.getItem("whichScope") == "child") {
        var url = window.location.pathname;
        var id = url.substring(url.lastIndexOf("/") + 1);
        // let formDataChildren = new FormData($("#user-edit_child")[0]);

        /** 18 june 2021
         * Author: Nilesh Matal
         * This Code is added to convert object name from forms.
         * 
         */
        let formDataset = {'id':id,
                      'first_name':'',
                      'last_name':'',

                      'birthdate':'',
                      'medical_issue':'',}

        let dataset = $('#user-edit_child').serialize();
        let splitdata = dataset.split('&')
        splitdata.forEach(element => {
          console.log(element)
          console.log(element.split('='))
          data = element.split('=');
          if (data[0] == "first_name_child") {

            formDataset.first_name = data[1]
          }
          if (data[0] == "last_name_child") {

            formDataset.last_name = data[1]
          }
          // if (data[0] == "school_name") {

          //   formDataset.school_name = data[1]
          // }
          // if (data[0] == "address_dropdown") {

          //   formDataset.address_details = data[1]
          // }
          // if (data[0] == "customer") {

          //   formDataset.customer = data[1]
          // }
          if (data[0] == "birthdate") {

            formDataset.birthdate = data[1]
          }
          if (data[0] == "medical_issue") {

            formDataset.medical_issue = data[1]
          }

        });
        var form_children_data = new FormData();

        for ( var key in formDataset ) {
          form_children_data.append(key, formDataset[key]);
        }
        console.log(form_children_data)
        $.ajax({
        url: "/student_data/",
        method: "PUT",
        enctype: "multipart/form-data",
        data: form_children_data,
        contentType: false,
        processData: false,
        async: false,
        success: function (data) {
            window.location.href = "/parents/";
        },
        error: function (data) {
            console.log(data);
        },
        });

        }

});

if (sessionStorage.getItem("whichScope") == "child") {
  $("#parent_edit_container").hide();
  $("#child_edit_container").show();
} else {
  $("#child_edit_container").hide();
  $("#parent_edit_container").show();
}
