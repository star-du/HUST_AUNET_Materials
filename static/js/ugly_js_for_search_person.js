/**
 * Search AJAX Module ---- Just make your experience comfortable!
 * 	* Search person
 * @param issues
 */

function show_result(persons){
	var bfr = "";
	for (var id in persons) {
		// ugliest lines in the whole world!!!
		bfr += "			<div class=\"card\">\
						<div class=\"card-content\">\
							<div class=\"row\">\
								<span class=\"card-title col s4 left\"><a href=\"/update/" + id + "\"\ class=\"light-green-text text-darken-4\">" + persons[id][0] + "</a></span>\
								<span class=\"card-title col s7\">" + id + "</span>\
							</div>\
							<div class=\"row\">\
								<table class=\"striped col s12\">\
									<tr>\
										<th>性别</th><td>" + persons[id][1] + "</td>\
										<th>QQ</th><td>" + persons[id][2] + "</td>\
									</tr>\
									<tr>\
										<th>电话</th><td>" + persons[id][3] + "</td>\
										<th>微信</th><td>" + persons[id][4] + "</td>\
									</tr>\
									<tr>\
										<th>应急联系方式</th><td>" + persons[id][5] + "</td>\
										<th>院系</th><td>" + persons[id][6] + "</td>\
									</tr>\
									<tr>\
										<th>班级</th><td>" + persons[id][7] + "</td>\
										<th>寝室</th><td>" + persons[id][8] + "</td>\
									</tr>\
									<tr>\
										<th>部门</th><td>" + persons[id][9] + "</td>\
										<th>组别</th><td>" + persons[id][10] + "</td>\
									</tr>\
									<tr>\
										<th>职务</th><td>" + persons[id][11] + "</td>\
										<th>加入时间</th><td>" + persons[id][12] + "</td>\
									</tr>\
								</table>\
							</div>\
						</div>\
					</div>\
					"
	}
	document.getElementById("result-table").innerHTML=bfr;
	// Toast if EMPTY RESULT
	if(bfr == ""){
		Materialize.toast("查询结果为空", 3000, "toast-warning")
	}
}




function search(){
	var search_data = {
		"d": document.getElementById("direction").value,
		"c": document.getElementById("content").value
	};
	$.ajax({
		type: 'GET',
		url: /searching_person/,
		data: search_data,
		dataType: 'json',
		success: function(data){
			show_result(data.result);
		},
		error: function(xhr, type){

		}
	});
	//location.href="/searching_person?d=" + direction + "&c=" + content;
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
