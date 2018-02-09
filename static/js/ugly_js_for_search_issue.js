/**
 * Search AJAX Module ---- Just make your experience comfortable!
 * 	* Search issues
 * @param issues
 */

function show_result(issues){
	var bfr = "";
	for (var id in issues) {
		console.log(issues[id]);
		// ugliest lines in the whole world!!!
		bfr += "			<div class=\"card\">\
						<div class=\"card-content\">\
							<div class=\"row\">\
								<span class=\"card-title col s4 left\">Issue&nbsp;No." + issues[id][0] + "</span>\
								<span class=\"card-title col s7\">" + issues[id][1] + "</span>\
							</div>\
							<div class=\"row\">\
								<div class=\"divider\"></div><br>\
								<div class=\"col s4\"><a href=\"/update_issue/" + id + "\" class=\"light-green-text text-darken-4\" title=\"单击以修改\"><b>" + issues[id][2] + "</b></a></div>\
								<pre class=\"col s8\" style=\"white-space:pre-wrap;word-wrap:break-word\">" + issues[id][3] + "</pre>\
								<br>\
							</div>\
						</div>\
					</div>\
"
	}
	document.getElementById("result-table").innerHTML=bfr;

	// Toast if EMPTY RESULT
	if(bfr == ""){
		Materialize.toast("查询结果为空", 3000, "toast-warning");

	}
}

function search(){
	var search_data = {
		"d": document.getElementById("direction").value,
		"c": document.getElementById("content").value
	};
	$.ajax({
		type: 'GET',
		url: '/searching_issue/',
		data: search_data,
		dataType: 'json',
		success: function(data){
			show_result(data.result);
		},
		error: function(xhr, type){

		}
	})
	//location.href="/searching_issue?d=" + direction + "&c=" + content;
}

/**
 * Support pressing Enter key to perform a search
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
		search();
	}

}
