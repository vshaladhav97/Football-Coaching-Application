const daysArray = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun', 'number of day(s) pass', 'Week Cost'];
var monthArr = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
var totalChildList;
var currentPageStartDate=null;
var currentWeekNumber=null;
var weekDisplayStr=null;
var finalPassCheckboxNames = [];
var weekCounting=null;
var course_type_name = localStorage.getItem("course_type_name")

function prepareDynamicWeekView(childList,weekDisplayStr){
    let bookingEle; 
    
    bookingEle = $('.week_booking').empty();
    bookingEle.append('<h2 class="heading">Week '+currentWeekNumber+'</h2>'
    + '<h3 class="show_date">'+weekDisplayStr+'</h3>');
    
    if(childList.data.length >0){
        if(currentWeekNumber === 1){
            bookingEle.append('<h5 class="sub_heading">Select a child from each name dropbox </h5>');
        } 
    
        bookingEle.append('<div class="table_responsive">');
        
        if(childList){
        var allChilds = new Array();
        $.each(childList.data, function(index, value){
            index++;
            allChilds.push('<div class="child">Child '+ index+'</div>');
        });
    
        $('<div class="first_tb" />').append(allChilds.join('')).appendTo('.table_responsive');
        bookingEle.append('</div>'
        + '</div>');
    
        var allChildNames = new Array();
        $.each(childList.data, function(index, value){
            index++;
            allChildNames.push('<div class="select_child"><span class="childName_'+index+'" value ="">'+ value.first_name +'</span><span class="primary-field primaryChild_'+index+'"></span></div>');
        });
    
        $('<div class="select_name_tb childHeader" />').append(allChildNames.join('')).appendTo('.table_responsive');
        bookingEle.append('</div>');
        let currentWeekObj=getCurrentWeekObj();
        
        $.each(daysArray, function(index, dayValue){
            index++;
            var allDays = new Array();
            if(dayValue == 'Week Cost'){
                allDays.push('<div class="child_day weekCostTxt"> Week '+currentWeekNumber+' Cost </div>');
            } else{
                allDays.push('<div class="child_day">'+ dayValue +'</div>');
            }
            
            var allDayCheckboxes = new Array();
            var numberPasses = new Array();
            var weekCosts = new Array();
            totalChildList = childList;
            var totalChilds = childList.data.length;
            $.each(childList.data, function(indexId, value){
                indexId++;
                if(dayValue == 'Sat' || dayValue == 'Sun'){
                    allDayCheckboxes.push('<div class="child_check"><input type="checkbox" class="checkbox-custom hideWeekend" id="" name="child-checkbox_'+indexId+'" value=""> <span class="checkbox-custom-dummy"></span> </div>');
                }else if(dayValue == 'number of day(s) pass'){
                    numberPasses.push('<div class="child_check"><span class = "child-pass-days_'+indexId+'">0 days</span> </div>');
                    if(totalChilds == indexId){
                        numberPasses.push('<div class="child_check"> </div>');
                        numberPasses.push('<div class="child_check"><span class = "child-pass-days_save_'+indexId+'"> Saved</span> </div>');
                    }
                }else if(dayValue == 'Week Cost'){
                    weekCosts.push('<div class="child_check"><span class = "child-cost-week_'+indexId+'">£ 0</span> </div>');  
                    if(totalChilds == indexId){
                        weekCosts.push('<div class="child_check total"><span class = "totalWeek-cost">£ 0</span> </div>');  
                        weekCosts.push('<div class="child_check saved"><span class = "savedTotalWeek-cost">£ 0</span> </div>');  
                    }
                }else{
                    let checked="";
                    if(isTheValueChecked(currentWeekObj,indexId,dayValue)){
                        checked="checked";
                    }
                    allDayCheckboxes.push('<div class="child_check"><input type="checkbox" '+checked+' class="checkbox-custom" id="" name="child-checkbox_'+indexId+'" value=""> <span class="checkbox-custom-dummy"></span></div>');
                }      
            
                let childObj=getExistingPerChildPerWeekObj(currentWeekObj.childArr ,indexId);
                $('.table_responsive').find('.number_pass').find('.child-pass-days_'+indexId+'')
                 .text((childObj.number_of_days_pass?childObj.number_of_days_pass:0)+' days');
            });

            if ( index % 2 == 0 && dayValue != 'number of day(s) pass') {
            $('<div class="select_name_tbs even weekBox" />').append(allDays.join(''))
            .append(allDayCheckboxes.join('')).appendTo('.table_responsive');
            } else if( index % 2 != 0 && dayValue != 'Week Cost'){
                $('<div class="select_name_tbs odd weekBox" />').append(allDays.join(''))
            .append(allDayCheckboxes.join('')).appendTo('.table_responsive');
            }
    
            if(dayValue == 'number of day(s) pass'){
                $(`<div class="select_name_tbs number_pass ${course_type_name}" />`).append(allDays.join(''))
                .appendTo('.table_responsive');
                
                $('<div class="d-flex in_child" />').append(numberPasses.join(''))
                .appendTo('.number_pass');
            }
    
            if(dayValue == 'Week Cost'){
                $('<div class="select_name_tbs week_pass" />').append(allDays.join(''))     
                .appendTo('.table_responsive');
    
                $('<div class="d-flex in_child" />').append(weekCosts.join(''))
                .appendTo('.week_pass');
            }
    
            bookingEle.append('</div>');       
        });
        //Appending total of child Weeks
        $.each(childList.data, function(index, value){
            index++;
            let childObj=getExistingPerChildPerWeekObj(currentWeekObj.childArr ,index);
            $('.table_responsive').find('.week_pass')
              .find('.child-cost-week_'+index+'').text('£ '+(childObj.cost ? childObj.cost:0));
        });
        
        $('.table_responsive').find('.week_pass')
            .find('.totalWeek-cost').text('£ '+currentWeekObj.totalAmountPerWeek?currentWeekObj.totalAmountPerWeek:0);
        $('.table_responsive').find('.week_pass')
            .find('.savedTotalWeek-cost').text('£ '+
                    currentWeekObj.totalDiscountPerWeek?currentWeekObj.totalDiscountPerWeek:0);

        }else{
            console.log("No child list obtained");
        }
    }
}

    

var startIntervalTime = new Date().getTime();
var interval = setInterval(function(){
    if(new Date().getTime() - startIntervalTime > 2000){
        clearInterval(interval);
        return;
    }
    disableDivs();
}, 500);     

  function disableDivs(){
    if(currentWeekNumber == 1){
        var weeks = $('.weekBox');
        $.each(weeks, function(index, value){
            if(index < startWeekBackDayCount){
                var allChecks = $(this).find('.child_check');
                $.each(allChecks, function(index, value){
                    $(this).find('.checkbox-custom').attr('disabled','true');
                })
            }
        });
    }

    if(currentWeekNumber == weekCounting){
        var weeks = $('.weekBox');
        $.each(weeks, function(index, value){
            index++;
            var total = 7 - endWeekForwardDayCount;
            if(index > total){
                var allChecks = $(this).find('.child_check');
                $.each(allChecks, function(index, value){
                    $(this).find('.checkbox-custom').attr('disabled','true');
                })
            }
        });
    }
 }

//Continue button logic
$('#continueBooking').on('click', function(e){
    calculateTheChildPerWeekRelatedValues(true);
});

//Back button - Added logic to render week details if exists.
$('#backBooking').on('click', function(e){
    calculateTheChildPerWeekRelatedValues(false);
});

function calculateTheChildPerWeekRelatedValues(movingForward){
    if(totalChildList){
        var totalAmountPerWeek = 0;
        var selectedCheckboxes;
        let childDataObj=totalChildList.data;

        for(let index=0 ; index<childDataObj.length; index++){
            let perChildSelected={};
            let value=childDataObj[index];
            var result = $('input[name="child-checkbox_'+(index+1)+'"]');
            
            let selectChkArr=[]
            result.each(function () {
                let perChildSelected={};
                let nameOfDay=$(this).closest('.select_name_tbs').find('.child_day').text();
                let isChecked= $(this).is(':checked');
                perChildSelected.nameOfDay=nameOfDay;
                perChildSelected.isChecked=isChecked;
                selectChkArr.push(perChildSelected);
                selectedCheckboxes += nameOfDay+"- ";
                selectedCheckboxes += isChecked+" ,";
            });
            // console.log('childId--',value.id, 'child Name -- ', value.first_name,
            // 'parentId--', value.customer,'===selected values--', selectedCheckboxes);
            let childObj = {}
            childObj.id=value.id;
            childObj.childId=(index+1);
            childObj.selectChkArr=selectChkArr;
            calculateChildAmountAndWeekTotal(totalAmountPerWeek,(index+1),childObj);
        }
        
        calculateDateAndWeekToRenderView(totalChildList,movingForward);
       // finalPassCheckboxNames = [];
        disableDivs();
    }else{
        console.log("No childlist available");
    }
}

function calculateChildAmountAndWeekTotal(totalAmountPerWeek,index,childObj){
    var numberOfPassTxt;
    var childWeekTotalTxt;
    var numberOfPass;
    var childWeekTotal;

    numberOfPassTxt = $('.child-pass-days_'+index+'').text().split(" ");
    numberOfPass = parseInt(numberOfPassTxt[0]);
    childWeekTotalTxt = $('.child-cost-week_'+index+'').text().split(" ");  
    
    childWeekTotal = parseInt(childWeekTotalTxt[1]);
    totalAmountPerWeek = totalAmountPerWeek + childWeekTotal;
    // console.log('numberOfPass==', numberOfPass, '--childWeekTotal--',childWeekTotal,
    //  '==totalAmountPerWeek--',totalAmountPerWeek);
    
    //Assuming position of the child never changes
    childObj.number_of_days_pass=numberOfPass;
    childObj.cost=childWeekTotal;
    childObj.primary=isPrimaryChild(childObj.childId);
    //Pending need to calculate this
    updatePerWeekBooking(childObj,null,null,null,null,null);

}

$(document).on("click", ".checkbox-custom" , function() {
   var checkboxName =  $(this).attr('name');
   var removedCheckBox;
   
   let finalPassCheckboxNames =getfinalPassCheckboxNames();

   if($(this).is(':checked')){  
        finalPassCheckboxNames.push(checkboxName);   
        // console.log(finalPassCheckboxNames);
   } else{
      if(finalPassCheckboxNames.indexOf(checkboxName) !== -1){
        finalPassCheckboxNames.splice(finalPassCheckboxNames.indexOf(checkboxName),1);
        removedCheckBox = checkboxName;
      }  
   }

   finalPassCheckboxNames.sort();
   updatePerWeekBooking(null,null,null,finalPassCheckboxNames);
    var current = null;
    var cnt = 0;

    for (var i = 0; i < finalPassCheckboxNames.length; i++) {   
        if (finalPassCheckboxNames[i] != current) {
            if (cnt > 0) {
                var newName = current.split('_');
                var childCheckboxId = newName[1];
                $('.table_responsive').find('.number_pass')
                .find('.child-pass-days_'+childCheckboxId+'').text(cnt+' days');

                calculateEveryChildWeekAmount(cnt, childCheckboxId);
            }
            current = finalPassCheckboxNames[i];
            cnt = 1;
        } else {
            cnt++;
        }
    }
    if (cnt > 0) {
        var newName = current.split('_');
        var childCheckboxId = newName[1];
        $('.table_responsive').find('.number_pass')
        .find('.child-pass-days_'+childCheckboxId+'').text(cnt+' days');
        
        calculateEveryChildWeekAmount(cnt, childCheckboxId);
    } 
    if(removedCheckBox && jQuery.inArray(removedCheckBox, finalPassCheckboxNames) === -1){
        var newName = removedCheckBox.split('_');
        var childCheckboxId = newName[1];
        $('.table_responsive').find('.number_pass')
        .find('.child-pass-days_'+childCheckboxId+'').text(0+' days');
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+0);
        
        checkHighestAmountAndDiscountCalculate();
        $('.table_responsive').find('.childHeader')
            .find('.primaryChild_'+childCheckboxId+'').text('');
    }   
});

function calculateEveryChildWeekAmount(cnt, childCheckboxId){
    if(cnt == 1){
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+parseInt($('#single_day_price').text()));
    }
    if(cnt == 2){
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+parseInt($('#two_day_price').text()));
    }
    if(cnt == 3){
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+parseInt($('#three_day_price').text()));
    }
    if(cnt == 4){
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+parseInt($('#four_day_price').text()));
    }
    if(cnt == 5){
        $('.table_responsive').find('.week_pass')
        .find('.child-cost-week_'+childCheckboxId+'').text('£ '+parseInt($('#five_day_price').text()));
    }

    checkHighestAmountAndDiscountCalculate();
}

function checkHighestAmountAndDiscountCalculate(){
    var childAmountArr = [];
    var amountDivArr = [];
    var numberPassDivArr = [];
    var numberPassArr = [];
    $.each(totalChildList.data, function(index, value){
        index++;
        $('.table_responsive').find('.childHeader').find('.primaryChild_'+index+'').text('');

        var numberPassDiv =  $('.table_responsive').find('.number_pass').find('.child-pass-days_'+index+'');
        numberPassDivArr.push(numberPassDiv);
        var passNum = numberPassDiv.text().split(" ");
        numberPassArr.push(parseInt(passNum[0]));

        var amountDiv = $('.table_responsive').find('.week_pass').find('.child-cost-week_'+index+'');
        amountDivArr.push(amountDiv);
        var amount = amountDiv.text().split(" ");
   
        childAmountArr.push(parseInt(amount[1]));
        $('.table_responsive').find('.childHeader').find('.primaryChild_'+index+'').text('');
    });

    var maxAmount = Math.max.apply(Math, childAmountArr);
    var maxPassCount = Math.max.apply(Math, numberPassArr);

    //To calculate total amount without discount
    var weekTotalWithoutDiscount = 0;
    $.each(childAmountArr, function(index, value){
        weekTotalWithoutDiscount = weekTotalWithoutDiscount + value;
    });
    // console.log('weekTotalWithoutDiscount==',weekTotalWithoutDiscount);

    //Remove max amount from Array to calculate discount
    if($.inArray(maxAmount, childAmountArr) !== -1){
        childAmountArr.splice(childAmountArr.indexOf(maxAmount), 1);
    }

    //calculate week total & saved amount
    calculateWeekTotalAndSavedAmount(childAmountArr,maxAmount,weekTotalWithoutDiscount);

    //To set primay child
   setPrimaryChild(numberPassDivArr, maxPassCount);
}

//calculate week total & saved amount
function calculateWeekTotalAndSavedAmount(childAmountArr,maxAmount,weekTotalWithoutDiscount){
    var weekTotalAmount = 0;
    $.each(childAmountArr, function(index, value){
        weekTotalAmount = weekTotalAmount + value;
    });

    var calcPrice = 0;
    var finalTotal = 0;
    var saveValue = 0;
    if(weekTotalAmount > 0){
        calcPrice = weekTotalAmount - ((weekTotalAmount/100) * 10 ).toFixed(2);
        finalTotal = maxAmount + calcPrice;
        //If we don't add 0 it becomes String eg "05.02" ideally should be 5.02
        saveValue = (weekTotalWithoutDiscount - finalTotal);
        if(saveValue>0){
            saveValue=Number(saveValue.toFixed(2));
        }else{
            saveValue = 0;
        }
    }else{
        finalTotal = maxAmount + calcPrice;
    }
    // console.log('weekTotalWithoutDiscount',weekTotalWithoutDiscount,'===calcPrice==',
    // calcPrice,'--finalTotal===',finalTotal, '>>>saveValue--',saveValue.toFixed(2));

    $('.table_responsive').find('.week_pass')
            .find('.totalWeek-cost').text('£ '+Number(finalTotal.toFixed(2)));
    
    $('.table_responsive').find('.week_pass')
    .find('.savedTotalWeek-cost').text('£ '+saveValue);
    
    updatePerWeekBooking(null,finalTotal,saveValue,null,null,null);
}

 //To set primay child
function setPrimaryChild(numberPassDivArr,maxPassCount){
    var flag = true;
    $.each(numberPassDivArr, function(index, value){
        var divValue = $(this).text().split(" ");
        if(parseInt(divValue[0]) == maxPassCount && flag){
            var divClassName = $(this).attr('class').split("_");
            $('.table_responsive').find('.childHeader')
            .find('.primaryChild_'+divClassName[1]+'').text('primary');
            flag = false;
        }
    });
}

//Calculation of date logic start
function calculateDateAndWeekToRenderView(childList,goingForward){
    let startDateOfWeek= null;
    let endDateOfWeek= null;
    if(currentPageStartDate==null){
        startDateOfWeek=getClosestMonday(startDateOfCourse);
        endDateOfWeek=getCommingSunday(startDateOfWeek);
        currentPageStartDate = startDateOfWeek;
        currentWeekNumber=1;
    }else if(currentPageStartDate!=null) {
        //Here we will always get the monday date in currentPageStartDate
        if(goingForward && currentWeekNumber<weekCounting){
            startDateOfWeek=getNextMonday(currentPageStartDate);
            endDateOfWeek=getCommingSunday(startDateOfWeek);
            currentWeekNumber=currentWeekNumber+1;
            currentPageStartDate = startDateOfWeek;
        }else if(!goingForward && (currentWeekNumber-1)>0){
            startDateOfWeek=getPreviousMonday(currentPageStartDate);
            endDateOfWeek=getCommingSunday(startDateOfWeek);
            currentWeekNumber=currentWeekNumber-1;
            currentPageStartDate = startDateOfWeek;
        }else if (goingForward == true && startDateOfWeek==null && endDateOfWeek==null){
            sessionStorage.setItem('perWeekbookingMainObj', JSON.stringify(perWeekbookingMainObj));
            window.location.href = "/order_summary/"
        }
    }
    // console.log('startDateOfWeek =='+startDateOfWeek+ '&& endDateOfWeek =='+endDateOfWeek);
    // console.log('currentWeekNumber =='+currentWeekNumber);
    if(startDateOfWeek && endDateOfWeek){
        let formattedWeekDisplayStr=formatDateAsExpected(startDateOfWeek,endDateOfWeek);
        updatePerWeekBooking(null,null,null,null,startDateOfWeek,endDateOfWeek);
        // console.log("Formatted String =="+formattedWeekDisplayStr);
        weekDisplayStr=formattedWeekDisplayStr;
        prepareDynamicWeekView(childList,formattedWeekDisplayStr);
    }
    currentWeekNumber==1? ($($('#backBooking')[0]).hide()): $($('#backBooking')[0]).show();
}

 function getClosestMonday(requestDate){
  let d = new Date(requestDate);
  var day = d.getDay(),
  diff = d.getDate() - day + (day == 0 ? -6:1);
  return new Date(d.setDate(diff));
}

function getCommingSunday(requestDate){
    let d = new Date(requestDate);
    var day = d.getDay(),
    diff = d.getDate() - day + (day == 0 ? -6:7);
    return new Date(d.setDate(diff));
}

function getPreviousMonday(requestDate){
    let dt = new Date(requestDate);
    dt.setDate( dt.getDate() - 7 );
    return new Date(dt);
}

function getNextMonday(requestDate){
    let dt = new Date(requestDate);
    dt.setDate( dt.getDate() + 7 );
    return new Date(dt);
}

function formatDateAsExpected(startDate,endDate){
    let responseString='';
    let nth = function(d) {
        if (d > 3 && d < 21) return 'th';
        switch (d % 10) {
          case 1:  return "st";
          case 2:  return "nd";
          case 3:  return "rd";
          default: return "th";
        }
      }
     let date = startDate.getDate();
     responseString+=date+nth(date);
     responseString+=" - ";

     date = endDate.getDate();
     let monthName=monthArr[endDate.getMonth()];
     responseString+=date+nth(date)+" of "+monthName+" "+endDate.getFullYear();
     return responseString;
}
//Calculation of date logic ends
function updatePerWeekBooking(childObj,totalAmountPerWeek,totalDiscountPerWeek,
    finalPassCheckboxNames,startDateOfWeek,endDateOfWeek){
    
    let totalCostCalculationOfAllWeeks=0;
    let perWeekArr= perWeekbookingMainObj.perWeekArr ?  
                        perWeekbookingMainObj.perWeekArr : [];

    //Setup per week details starts
    let perWeekObj = getExistingPerWeekObj(perWeekArr);
    perWeekObj.weekNumber=currentWeekNumber;
    perWeekObj.weekDisplayTxt=weekDisplayStr;
    if(childObj){
        let childArr = perWeekObj.childArr ? perWeekObj.childArr : [];
        let singleChildPerWeekObj=getExistingPerChildPerWeekObj(childArr,childObj.childId);

        if(singleChildPerWeekObj.position!=null){
            childObj.position=singleChildPerWeekObj.position;
            childArr[singleChildPerWeekObj.position]=childObj;
        }else{
            childObj.position=childArr.length;
            childArr.push(childObj);
        }
        perWeekObj.childArr=childArr;
    }

    if(totalAmountPerWeek!=null){
        perWeekObj.totalAmountPerWeek=totalAmountPerWeek?totalAmountPerWeek:0;
    }
    if(totalAmountPerWeek!=null){
        perWeekObj.totalDiscountPerWeek=totalDiscountPerWeek ?totalDiscountPerWeek:0 ;
    }

    if(finalPassCheckboxNames){
        perWeekObj.finalPassCheckboxNames=finalPassCheckboxNames;
    }

    if(startDateOfWeek){
        perWeekObj.week_start_date=convertDateToStr(startDateOfWeek,'YYYY-MM-DD');
    }

    if(endDateOfWeek){
        perWeekObj.week_end_date=convertDateToStr(endDateOfWeek,'YYYY-MM-DD');
    }

    //If already exist there will be a position in the array
    if(perWeekObj.position!=null){
        perWeekArr[perWeekObj.position]=perWeekObj;
    }else{
        perWeekObj.position=perWeekArr.length;
        perWeekArr.push(perWeekObj);
    }

    //Setup per week details ends
    perWeekbookingMainObj.event_type_id=eventTypeId;
    perWeekbookingMainObj.total_cost=0;
    perWeekbookingMainObj.discounted_amount=0;
    perWeekbookingMainObj.perWeekArr=perWeekArr;
    setFinalCostAndDiscountOfAllWeeks(perWeekArr);
    // console.log(perWeekbookingMainObj);
}

function getExistingPerWeekObj(perWeekArr){

    if(perWeekArr){
        for(let i=0;i<perWeekArr.length ; i++){
            if(perWeekArr[i] && perWeekArr[i].weekNumber && perWeekArr[i].weekNumber==currentWeekNumber){
                return perWeekArr[i];
            }
        }
    }
    return {};
}


function getExistingPerChildPerWeekObj(childArr,childId){
    if(childArr && childId){
        for(let i=0;i<childArr.length ; i++){
            if(childArr[i] && childArr[i].childId && childArr[i].childId==childId){
                return childArr[i];
            }
        }
    }
    return {};
}

function isTheValueChecked(perWeekObj,childId,dayName){
    if(perWeekObj){
        let childArr=perWeekObj.childArr;
        if(childArr && dayName){
            for(let i=0;i<childArr.length;i++ ){
                let childObj=childArr[i];
                if(childObj && childId!=null && childObj.childId==childId){
                    return checkTheDayNameAndValue(childObj,dayName);
                }
            }
        }
    }
    return false;
}

function getCurrentWeekObj(){
    let perWeekArr= perWeekbookingMainObj.perWeekArr ?  
    perWeekbookingMainObj.perWeekArr : [];
    return getExistingPerWeekObj(perWeekArr);
}

function checkTheDayNameAndValue(childObj,dayName){
    let selectChkArr=childObj.selectChkArr;
    if(selectChkArr){
        for(let j=0;j<selectChkArr.length;j++){
            let selectionObj=selectChkArr[j];
            if(selectionObj!=null && selectionObj.nameOfDay==dayName){
                return selectionObj.isChecked;
            }
        }
    }
    return false;
}

function weeksBetween(d1, d2) {
    let oneDayMilliSec=24 * 60 * 60 * 1000;
    d2=addDays(d2, days);
    let weekCount=Math.round((d2 - d1) / (7 *oneDayMilliSec ));
    let weekRemain=(d2 - d1)%((7 * oneDayMilliSec));
    return weekCount+weekRemain;
}

function addDays(date, days) {
   var result = new Date(date);
   result.setDate(result.getDate() + days);
   return result;
}


function setFinalCostAndDiscountOfAllWeeks(perWeekArr){
    let totalOfAllWeekAmount=0;
    let totalOfAllDiscountAmount=0;
    $.each(perWeekArr,function(index, perWeekObj){
        if(perWeekObj.totalAmountPerWeek && !Number.isNaN(perWeekObj.totalAmountPerWeek)){
            totalOfAllWeekAmount+=perWeekObj.totalAmountPerWeek;
        }
        if(perWeekObj.totalAmountPerWeek && !Number.isNaN(perWeekObj.totalDiscountPerWeek)){
            totalOfAllDiscountAmount+=perWeekObj.totalDiscountPerWeek;
        }
    });
    perWeekbookingMainObj.total_cost=totalOfAllWeekAmount;
    perWeekbookingMainObj.discounted_amount=totalOfAllDiscountAmount;
}


function getChildObjIfExist(){
    let perWeekArr= perWeekbookingMainObj.perWeekArr ?  
    perWeekbookingMainObj.perWeekArr : [];
    return getExistingPerWeekObj(perWeekArr);
}

function getfinalPassCheckboxNames(){
    let perWeekObj=getCurrentWeekObj();
    return (perWeekObj.finalPassCheckboxNames ? perWeekObj.finalPassCheckboxNames : []);
}

function isPrimaryChild(childId){
    let primaryFields=$('.primary-field');
    let isPrimary=false;
    if(primaryFields){
     $.each(primaryFields , function(index,value){
        if($(primaryFields[index]).text() && $(primaryFields[index]).text()=='primary'
            && (index+1)==childId){
            isPrimary=isPrimary|| true;      
        }
        index++;
     });
    }
    return isPrimary;
}

function convertDateToStr(date,formatterStr){
    return moment(date).format(formatterStr);
}

$(document).ready(function () {
    var startevtdate =getClosestMonday(startDateOfCourse);
    var endevtdate=getCommingSunday(endDateOfCourse);
    weekCounting = Math.round((endevtdate - startevtdate) / (7 * 24 * 60 * 60 * 1000));
    // console.log('startevtdate--=',startevtdate, '--endevtdate==',endevtdate,'===weekCounting--',weekCounting);

});