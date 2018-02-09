function change_searchbox() {
    $("#content-wrap").fadeOut(250);

    switch ($("#direction").val()) {
        case 'date':
        var bfr ="<input name=\"content\" id=\"content\" type=\"date\" class=\"datepicker\" onchange=\"search()\" placeholder=\"请选择日期\" required>";
            $("#content-wrap").html(bfr);
            $('.datepicker').pickadate({
                selectMonths: true,
                selectYears: 15
            });
            break;

        case 'depart':
            var bfr = "\
            <select name=\"content\" id=\"content\" onchange=\"search()\" required>\
            <option value=\"苟\" disabled selected>请选择部门</option>\
            <option value=\"财务部\">财务部</option>\
            <option value=\"秘书部\">秘书部</option>\
            <option value=\"人力资源部\">人力资源部</option>\
            <option value=\"社团部\">社团部</option>\
            <option value=\"行政监察部\">行政监察部</option>\
            <option value=\"外联部\">外联部</option>\
            <option value=\"公共关系部\">公共关系部</option>\
            <option value=\"宣传部\">宣传部</option>\
            <option value=\"媒体部\">媒体部</option>\
            <option value=\"思存工作室\">思存工作室</option>\
            <option value=\"新媒体工作室\">新媒体工作室</option>\
            <option value=\"社团外联企划小组\">社团外联企划小组</option>\
            <option value=\"文艺拓展部\">文艺拓展部</option>\
            <option value=\"其它\">其它</option>\
            </select>";
            $("#content-wrap").html(bfr);
            $('select').material_select();
            // TODO: placeholder should be displayed in grey
            break;

        case 'title':
            var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"请输入表格标题\" onkeypress=\"EnterKeyToSearch()\" required>";
            $("#content-wrap").html(bfr);
            break;

        case 'id':
            var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"请输入社联编号\" onkeypress=\"EnterKeyToSearch()\" required>";
            $("#content-wrap").html(bfr);
            break;

        case 'name':
            var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"请输入姓名\" onkeypress=\"EnterKeyToSearch()\" required>";
            $("#content-wrap").html(bfr);
            break;

        case 'apart':  // TODO: use <select>
            var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"公寓-楼栋号-房间号\" onkeypress=\"EnterKeyToSearch()\" required>";
            $("#content-wrap").html(bfr);
            break;

        case 'school':  // TODO: use <select>
            var bfr = "<input name=\"content\" id=\"content\" type=\"text\" class=\"black-text\" placeholder=\"请输入学院\" onkeypress=\"EnterKeyToSearch()\" required>";
            $("#content-wrap").html(bfr);
            break;

        default:
            Materialize.toast("DON'T MESS UP WITH MY CODE!", 3000, "error");
            break;
    }

    $("#content-wrap").fadeIn(250);
}
