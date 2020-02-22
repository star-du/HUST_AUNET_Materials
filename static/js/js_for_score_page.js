function count_now(name) {
    $("#"+name).each(function(index, this_form) {
        result = count_each(name);
        // TODO: is getElementsByTagName() safe enough??
        this_form.getElementsByTagName("span")[0].innerHTML=result[0];
        this_form.getElementsByTagName("span")[1].innerHTML=result[1];
    });
}


function count_each(name) {
    var self_total = 0, total = 0;
    var i;
    var f = document.getElementsByName(name);
    for (i = 1; i <= 5; i++) {
        self_total += Number(f[i].value);
    }
    for (i = 1; i <= 9; i++) {
        total += Number(f[i].value);
    }
    return [self_total, total];
}


function prefill() {
    var range = $("#input-wrap").children();
    // console.log(range.length);
    for (var i = 0; i < range.length; i++) {
        count_now(range[i].attributes.name.value);
    }
}


function submit_now(name, e) {
    var f = document.getElementsByName(name);
    for (var each = 1; each < 10; each++) {
        if (f[each].value === '') {
            Materialize.toast(
                $("<div>分数不能为空！</div>"), 3000, 'toast-warning');
            return;
        }
    }
    // console.log(f);
    // JSON data is sent in RANDOM order!!!
    var data = {
        "name": name,
        "dim-self": f[1].value,
        "act-self": f[2].value,
        "act-num": f[3].value,
        "dly-self": f[4].value,
        "dly-act": f[5].value,
        "mntr-dim": f[6].value,
        "mntr-act": f[7].value,
        "attd": f[8].value,
        "bonus": f[9].value,
        "total": f[11].innerHTML
    };
    $.ajax({
        type: 'POST',
        url: /scoring_page/,
        data: JSON.stringify(data),
        contentType: 'application/json; charsef=UTF-8',
        dataType: 'json',
        success: function(data){
            var result = data.result;
            var i;
            var f = document.getElementsByName(result["name"]);
            // TODO: code structue could be simplified using jQuery
            f[1].value = result["dim-self"];
            f[2].value = result["act-self"];
            f[3].value = result["act-num"];
            f[4].value = result["dly-self"];
            f[5].value = result["dly-act"];
            f[6].value = result["mntr-dim"];
            f[7].value = result["mntr-act"];
            f[8].value = result["attd"];
            f[9].value = result["bonus"];
            toast_msg =
            Materialize.toast(
                $("<div>成功写入 "+result['name']+" 的分数！</div>"),
                3000, 'toast-success');
            $("ul li a[href=#"+result['name']+"]").attr("class", "teal-text")
        },
        error: function(xhr, type){
            Materialize.toast(
                $("<div>数据交换失败！</div>"),
                3000, 'toast-error'
            )
        }
    });
}



// TODO: prevent inputing characters
