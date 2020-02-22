/**
 * ###################### FREE-TIME PICKER CONTROLLER ######################
 * Created by AnCla on 2017/4/26 0026.
 * TODO: *** Fill JSDoc, add instruction of @param id_of_picker. ***
 */

/**
 * @CORE-FUNCTION
 * Act the free time picker when you click a cell.
 *  - Change color
 *  - Mark your chosen free time cell with attr.
 * @param cellID  The cell you clicked.
 */
function handleFreeTimePick(cellID, id_of_picker){
    var selector = "[id='" + id_of_picker + "'] [id='" + cellID + "']";

    var cell = $(selector);
    if(cell.attr("freetime_checked") == "yes"){
        cell.attr("freetime_checked", "no");
        cell.css("background-color", "#FFFFFF");
    }
    else{
        cell.attr("freetime_checked", "yes");
        cell.css("background-color", "#4db6ac")
    }
}


/**
 * @CALLBACK-Function-Required
 * Analyse free time table, gather your picked free time value,
 *  and submit them to database with your defined callback function.
 * @CALLBACK-FUNCTION-Format
 *      A normal function with one parameter: result.
 *      Our gathered result will directly pass into it, and it will be called finally.
 * @param method_to_background: Your callback function's name.
 *      NOTICE: Just function name. Parameter isn't required.
 */
function submitFreeTimePick(method_to_background, id_of_picker){
    /** TODO: Result may duplicate / even corrupt when more than two pickers in one page, if they are all read-write. **/

    var tds = document.getElementsByName("free-time-picker");
    var result = [];

    for(var i=0; i<tds.length; i++){
        var selector = "[id='" + id_of_picker + "'] [id='" + tds[i].id + "']";

        var cell = $(selector);
        if(cell.attr("freetime_checked") == "yes"){
            result.push(tds[i].id)
        }
    }

    //For debug
    //alert("已统计的空闲时间如下：\n" + result.toString());
    console.log(tds.length);

    // Call your defined callback method
    method_to_background(result)

}

/**
 * Clear the free time picker. This is benefit for refilling the table.
 */
function clearFreeTimePick(id_of_picker){
    var tds = document.getElementsByName("free-time-picker");
    for(var i=0; i<tds.length; i++){
        var selector = "[id='" + id_of_picker + "'] [id='" + tds[i].id + "']";

        var cell=$(selector);
        cell.attr("freetime_checked", "no");
        cell.css("background-color", "#FFFFFF")
    }
}


/**
 * Initialize free time picker.
 * @param id_of_picker
 */
function initFreeTimePick(id_of_picker){

    const name_of_picker_cell = "free-time-picker";

    var tds = document.getElementsByName(name_of_picker_cell);

    for(var i=0; i<tds.length; i++)
    {
         //$("#"+tds[i].id).attr("onclick","handleFreeTimePick('"+tds[i].id+"')")
         //   .attr("freetime_checked", "no")

         var selector = "[id='" + id_of_picker + "'] [id='" + tds[i].id + "']";
         $(selector).attr("onclick","handleFreeTimePick('"+tds[i].id+"', '"+ id_of_picker + "')")
                     .attr("freetime_checked", "no")
    }


}


function initFreeTimePick_ReadOnly(id_of_picker){
    const name_of_picker_cell = "free-time-picker";

    var tds = document.getElementsByName(name_of_picker_cell);

    for(var i=0; i<tds.length; i++)
    {
         //$("#"+tds[i].id).attr("onclick","handleFreeTimePick('"+tds[i].id+"')")
         //   .attr("freetime_checked", "no")

         var selector = "[id='" + id_of_picker + "'] [id='" + tds[i].id + "']";
         $(selector).attr("freetime_checked", "no")
    }
}
