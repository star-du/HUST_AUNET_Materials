/**
 * Created by AnCla on 2017/2/9 0009.
 */
function clearFlash(){
    $.ajax({
        type: 'GET',
        url: '/clear_flash/',
        success: function(data){
            console.log(data.result['msg']);
        },
        error: function(){}
    })
}