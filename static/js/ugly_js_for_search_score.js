/**
 * Search AJAX Module ---- Just make your experience comfortable!
 *     * Search issues
 * @param issues
 */

function show_result(score){
    var bfr = "";
    for (var each in score) {
        // ugliest lines in the whole world!!!
        bfr += ("<li class=\"collection-item\"><span><a href=\"/score_page/" + score[each].title + "\" class=\"teal-text\" style=\"font-size1.4em\">" + score[each].title + "</a>&nbsp;&nbsp;&nbsp;&nbsp;of " + score[each].depart + "&nbsp;&nbsp;&nbsp;&nbsp;@ " + score[each].date + "</span><a href=\"/downloading/" + score[each].title + "\" class=\"secondary-content\"><i class=\"small material-icons\">file_download</i></a><a  href=\"#!\" class=\"secondary-content\" onclick=\"delete_file(\'/deleting/" + score[each].title + "\')\"><i class=\"small material-icons\">delete</i></a></pre></li>");
    }
    if (bfr == "") {
        document.getElementById("result-container").style.display="none";
        Materialize.toast("查询结果为空", 3000, "toast-warning")
    } else {
        document.getElementById("result-container").style.display="block";
        document.getElementById("result-container").innerHTML=bfr;
    }

}

function search(){
    var search_data = {
        "d": document.getElementById("direction").value,
        "c": document.getElementById("content").value
    };
    $.ajax({
        type: 'GET',
        url: /searching_score/,
        data: search_data,
        dataType: 'json',
        success: function(data){
            show_result(data.result);
        },
        error: function(xhr, type){
        }
    });
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

function delete_file(url) {
    // TODO: write my own confirm window
    var s = confirm("删除后将不可恢复！确认要删除吗？");
    if (s == true) {
        // console.log("deletion comfirmed!");
        location.href=url;
    } else {
        // console.log("deletion declined!");
    }
}
