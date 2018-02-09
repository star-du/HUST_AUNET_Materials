

/** ###################### DATABASE RENDERER SECTION ###################### **/

function submit_freetime_to_background(result)
{
    //TODO: 接下来可以将统计信息发往后台了。就用AJAX。
    var data={
        result: result.toString(),
        id: document.getElementById("id").innerText,
        name: document.getElementById("name").innerText,
    };
    $.ajax({
        type: 'POST',
        url: '/submit_freetime/',
        data: data,
        dataType: 'json',
        success: function(data){
            //TODO: 后台要回传一些数据，如处理成功的提示。
            //TODO: 但是具体如何处理，还要取决于怎么样设计录入部分（自动接续逐一录入，还是每次都要重新检索）
            searchPerson(true);     // 刷新. 所设参数为refresh_only，标示这仅仅是刷新而非人员检索

            /** Show and log messages
             *  Note: backMessage[] is a JSON-ified dict defined by background.
             * **/
            console.log("Chosen free time:" + data.backMessage['free_time']);

            if(data.backMessage['errorlevel'] == true){
                showInpageToast(data.backMessage['message'], "success");
            }
            else{
                showInpageToast(data.backMessage['message'], "error")
            }

            if(data.backMessage['sub_message']){
                showInpageToast(data.backMessage['sub_message']);
            }
            //Materialize.toast(data.backMessage['message'], 4000, "toast-info")
        },
        error: function(xhr, type){
            //Show a toast that we have bumped into an error
            showInpageToast("啊哦。。连接出错了。。马上戳思存的小伙伴吧！", 'error');
        }
    })
}

/**
 * Query a person's free time from database.
 * @param refresh_only: Set true if you only use this function for refreshing.
 * @returns {number} -1 if fails.
 * @dependency show_person(data).
 */
function searchPerson(refresh_only)
{
    var search_bar = document.getElementById("search-bar");
    var data = {
        depart: search_bar.getElementsByTagName("select")[0].value,
        direction: search_bar.getElementsByTagName("select")[1].value,
        content: search_bar.getElementsByTagName("input")[2].value
    };
    // console.log(data);
    if (data['depart'] == '' || data['direction'] == '' || data['content'] == '') {
        console.log("Invalid search!");
        //Give a toast
        showInpageToast("无效检索，请检查关键字！", "warning");
        return -1;
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/get_person_freetime/',
            data: data,
            dataType: 'json',
            success: function(data) {
                // console.log(data);
                if (show_person(data.result)) {
                    show_freetime(data.freetime);
                    // No need to show this toast if you use this func to refresh
                    if(!refresh_only)
                        showInpageToast("人员已检索到。现在可以开始编辑了", "success");
                }
                else {
                    showInpageToast("未检索到成员！", "warning");
                }
            },
            error: function(xhr, type) {
                //Show a toast that we have bumped into an error
                showInpageToast("啊哦。。连接出错了。。马上戳思存的小伙伴吧！", 'error');
            }
        });
    }
}


/**
 * @INNER-TOOL
 * After querying a person, parse the returned AJAX data from the backend, and generate the following data:
 *  - Name
 *  - ID
 * Then, give a result of found or not.
 * This function is used by searchPerson() to determine if we should render and toast, or not.
 * @param data
 *      AJAX data from backend.
 * @returns {number}
 *      If found, return 1, also print Name and ID on the top of free time picker;
 *      If not found, return 0 instead.
 */
function show_person(data) {
    var target_range = document.getElementsByName("search-result")[0];
    var target = target_range.getElementsByTagName("span");
     console.log(data);
    target[0].innerText = data[1];
    target[1].innerText = data[0];
    if (data[0] != "") {
        console.log("This person is in db!");
        return 1;
    }
    else {
        return 0;
    }
}


/**
 * Render a person's recorded free time (if have) to the free time picker.
 * @param data
 */
function show_freetime(data) {
    var target_range = document.getElementsByName("free-time-picker");
    console.log(data);
    // TODO: only loop 4 times...
    /*
    for (var each in target_range) {
    var target = target_range[each];
    console.log(data[each+1]);
    if (data[each+1] == 0) {
    $(target).attr("freetime_checked", "no");
    $(target).css("background-color", "#FFFFFF");
}
else if (data[each+1] == 1) {
$(target).attr("freetime_checked", "yes");
$(target).css("background-color", "#4db6ac");
}
}
*/
    // var tds = document.getElementsByName("free-time-picker");
    for (var i = 0; i < target_range.length; i++) {
        var cell = $("#" + target_range[i].id);
        if (data[i+1] == 0 || data.length == 0) {
            cell.attr("freetime_checked", "no");
            cell.css("background-color", "#FFFFFF");
        } else if (data[i+1] == 1) {
            cell.attr("freetime_checked", "yes");
            cell.css("background-color", "#4db6ac");
        }
    }



}


/** ###################### ADDITIONAL TWEAK FEATURES ###################### **/

/**
 * Press ENTER key to perform a search. This is a must for every mature sites.
 * @constructor
 */
function EnterKeyToSearch() {
	var key;
	if(window.event)
		key = event.keyCode;
	else if(event.which)
		key = event.which;
	var keychar = String.fromCharCode(key);

	if (keychar == "\r"){
		console.log("SEARCHBOX: Enter key pressed");
		searchPerson();
	}

}
