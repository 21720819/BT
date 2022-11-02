
// 채팅세부 목록 들어오면 스크롤 맨 아래로 고정
var scrollWant = document.getElementById("chat-messages"); 
scrollWant.scrollTop = scrollWant.scrollHeight;

//text area 입력되면 늘어남
function resize(obj) {
    obj.style.height = '1px';
    height = obj.scrollHeight;
    obj.style.height = (12 + obj.scrollHeight) + 'px';
}


function reload(){  
    $("#chats").load(window.location.href + "#chats");
}


/* input에 입력된 값 로컬스토리지에 저장하기 */
function saveValue(e){
    var id = e.id;
    var val = e.value;
    localStorage.setItem(id, val);
}

/* 로컬스토리지에 저장된 값으로 input 채우기 */ 
function getSavedValue(v){
    if(!localStorage.getItem(v)){
        // 사용자가 입력하지 않았다면 defualt 값을 반환 
        return v.value;
    }
    return localStorage.getItem(v);
}






function send_message(){
    sendMsgObj($('#tx_send').val());
    return false; 
}



$(function() {
$('textarea').on('keydown', function(event) {
    if (event.keyCode == 13)
        if (!event.shiftKey){
            event.preventDefault();
            send_message();

        }

})});





function button_click() {
    alert("you pressed submit button!");
}