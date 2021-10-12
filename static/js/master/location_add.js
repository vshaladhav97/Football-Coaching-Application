$('#location_submit').hide();
$('.add_venue_btn').on('click', function () {
    $('#location_submit').show();
});

// $('input[type=radio][name=new_company_button]').change(function() {
//     alert("hello")
// });



function checkForm(form) {

    if ($("#company").val() == "") {
        $('#company').parent().append('<span class="error">Please enter company. <span style="color:red;">*</span></span>').addClass("has-error");
        return false;
    }

    if ($("#venue_name").val() == "") {
        $('#venue_name').parent().append('<span class="error">Please enter venue name.  <span style="color:red;">*</span></span>').addClass("has-error");
        return false;
    }

    if ($("#street").val() == "") {
        $('#street').parent().append('<span class="error">Please enter street name.  <span style="color:red;">*</span></span>').addClass("has-error");
        return false;
    }

    if ($("#town").val() == "") {
        $('#town').parent().append('<span class="error">Please enter town.  <span style="color:red;">*</span></span>').addClass("has-error");
        return false;
    }

    if ($("#post_code").val() == "") {
        $('#post_code').parent().append('<span class="error">Please enter post code.  <span style="color:red;">*</span></span>').addClass("has-error");
        return false;
    }

}

$("#myModal").on("hidden.bs.modal", function () {
    window.location.href = "/location_list/"
});

function addVenueSection() {
    var counter = $('#counter').val();
    if (parseInt(counter) < 10) {
        var myHtml = "";
        $.ajax({
            type: 'get',
            url: '/course_type/',
            data: {

            },
            success: function (data) {
                jQuery.each(data.data, function (i, item) {
                    myHtml += "<input type='checkbox' name='course_type[" + parseInt(counter) + "]' value='" + item.id + "'> " + item.course_name + "<br>";
                });
                html = `<div class="col-md-6 locations_add_remove">
                            <div class="pad_30">
                            <span class="fa fa-trash"></span>
                            <div class="form-group row" style="margin-top: 0px;">
                                <label for="venue_name" class="col-sm-4 col-form-label">Venue name:  <span style="color:red;">*</span></label>
                                <div class="col-sm-8">
                                    <input type="text" class="form-control" id="venue_name" name="venue_name" required>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top: 0px;">
                                <label for="street" class="col-sm-4 col-form-label">Street:  <span style="color:red;">*</span></label>
                                <div class="col-sm-8">
                                    <input type="text" class="form-control" id="street" name="street" required>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top:0px;">
                                <label for="town" class="col-sm-4 col-form-label">City / Town:  <span style="color:red;">*</span></label>
                                <div class="col-sm-8">
                                    <input type="text" class="form-control" id="town" name="town" required>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top:0px;">
                                <label for="post_code" class="col-sm-4 col-form-label">Post code:  <span style="color:red;">*</span></label>
                                <div class="col-sm-8">
                                    <input type="text" class="form-control" id="post_code" name="post_code" required placeholder="ex M43 7AA" maxlength="7"/>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top:0px;">
                                <label for="playing_surface" class="col-sm-4 col-form-label">Playing surface:  <span style="color:red;">*</span></label>
                                <div class="col-sm-8">
                                    <select class="form-control playing_surface" name="playing_surface" id="playing_surface">

                                    </select>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top:0px;">
                                    <label for="playing_surface" class="col-sm-6 col-form-label">This venue is suitable for ?:<br>
                                        ${myHtml}
                                    </label>
                            </div>
                        </div>
                    </div>`

                $.ajax({
                    type: 'get',
                    url: '/playing_surface/',
                    data: {

                    },
                    success: function (data) {
                        jQuery.each(data.data, function (i, item) {
                            $('.playing_surface').append("<option value=" + item.id + ">" + item.surface + "</option>")
                        });
                    },
                    error: function (data) {
                        console.log(data);
                        //                $('#error-msg').text(data.responseJSON.status);
                    },
                });
                $('#venue-section').append(html);
                $('.locations_add_remove .pad_30 .fa.fa-trash').on('click', function () {
                    $(this).parents('.locations_add_remove').remove();
                });
            },
            error: function (data) {
                console.log(data);
                //                $('#error-msg').text(data.responseJSON.status);
            },
        });
    }
    else {
        $('#venue-add').css('display', 'none');
    }
    counter++;
    console.log(counter, "Count");
    $('#counter').val(counter);
    console.log(myHtml);

}


$.ajax({
    type: 'get',
    url: '/company_dropdown_list/',
    data: {

    },
    success: function (data) {
        jQuery.each(data, function (i, item) {   
                                html = 
                            `
                            
                            
                            <option id="${item.id}" onclick="filter_coach(${item.id})" value="${item.id}">${item.company_name}</option>
                            
                            `
                            $("#company_name").append(html);
                            
                            });
    },
});










$('#location_submit').on('click', function () {

    validation = checkForm();
    if (validation == false) {
        return false;
    }

    let formData = new FormData($("#location-add")[0]);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null) {
        window.location.href = "/"
    }

    $.ajax({
        url: "/locations/",
        method: "POST",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data: formData,
        contentType: false,
        processData: false,
        async: false,
        success: function (data) {
            window.location.href = "/location_list/"
        },
        error: function (data) {
            console.log(data);
        },
    });
    document.getElementById('post_code').addEventListener('input', function (e) {
        alert('in')
        var $field = $(this),
            val = this.value,
            $thisIndex = parseInt($field.data("idx"), 10);
        if (this.validity && this.validity.badInput || isNaN(val) || $field.is(":invalid")) {
            this.value = inputQuantity[$thisIndex];
            return;
        }
        if (val.length > Number($field.attr("maxlength"))) {
            val = val.slice(0, 9);
            $field.val(val);
        }
        inputQuantity[$thisIndex] = val;
        // e.target.value = e.target.value.replace(/[^[A-Z]]/g, '').replace(/(.{3})/g, '$1 ').trim();
    });
});


$("[name=select]").change(function(){
    console.log('button clicked')
    $("#newCompany").toggle($("[name=select]").index(this)===0);
    var cacheDom;
    let html = `
    <div class="col-md-12 " id="addCompany">
        <div class="form-group d-flex">
            <label for="company" class="col-form-label"><strong>Company: <sup
                        style="color: red;">*</sup></strong></label>
            <div class="" style="margin-left: 5px;">
                <input type="text" class="form-control" id="company" name="company">
            </div>
        </div>
    </div>`
    if($("[name=select]").index(this)===0) {
    
            if ("#newCompany" != '' ){
                $("#addCompany").remove();
                $('#newCompany').append(html);
        
            }
  
        $('div[id*=getCompany]').remove();
    }

    let html2 = ` <div class="col-md-12 " id="getCompany" style="display: block;">
                                    
    <label  class="col-form-label"><strong>New Company: <sup
        style="color: red;">*</sup></strong>
      <select lass="form-control" id="company_name"
      name="company_name" required>
        <option>Select Company Name</option>
          </select>
    </label>
  </div>`
  
  $("#existingCompany").toggle($("[name=select]").index(this)===1);
  if($("[name=select]").index(this)===1){
      // newCompany
      console.log('--s')
      // $("#form_body").clone().find('div .newCompany').remove()
      // $(".locations_").remove();
      // cacheDom = $('#newCompany');
      if ("#existingCompany" != '' ){

          $("#getCompany").remove();
          
          $('#existingCompany').append(html2);
          GetCompanyName();
      }
      $('div[id*=addCompany]').remove();


  }
  });

function GetCompanyName(){
    $.ajax({
        type: 'get',
        url: '/company_dropdown_list/',
        data: {
    
        },
        success: function (data) {
            jQuery.each(data, function (i, item) {   
                                    html = 
                                `
                                
                                
                                <option id="${item.id}" onclick="filter_coach(${item.id})" value="${item.id}">${item.company_name}</option>
                                
                                `
                                $("#company_name").append(html);
                                
                                });
        },
    });
}