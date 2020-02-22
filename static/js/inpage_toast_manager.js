/**
 * Created by AnCla on 2017/4/18 0018.
 */

function showInpageToast(msg, ctg)
{
    var message = {
														// TODO: |safe 标签不管用
        text: msg,
        category: ctg
    };
    var $messageHTML = $("<div>" + message.text + "</div>");
    switch (message.category) {
        case "error":
            Materialize.toast($messageHTML, 4000, "toast-error");
            break;
        case "success":
            Materialize.toast($messageHTML, 3000, "toast-success");
            break;
        case "warning":
            Materialize.toast($messageHTML, 3000, "toast-warning");
            break;
        default:
            Materialize.toast($messageHTML, 3000, "toast-info");
    }

}
