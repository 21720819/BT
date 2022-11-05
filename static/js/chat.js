
// 채팅세부 목록 들어오면 스크롤 맨 아래로 고정
var scrollWant = document.getElementById("chat-messages"); 
scrollWant.scrollTop = scrollWant.scrollHeight;


window.onpageshow = function(event) {
    if ( event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        location.reload();

    }
}

function change_time(unix_time){
    var date = new Date(unix_time);
    var hour = date.getHours();
    var minute = date.getMinutes();
    if (minute < 10)
        minute = "0"+minute
    var hour_Min = hour+":"+minute
    return hour_Min
}

function scrollDown(){
    var scrollWant = document.getElementById("chat-messages"); 
    scrollWant.scrollTop = scrollWant.scrollHeight;
}


function init_home(application_id, user_id){

    var sb = new SendBird({appId: application_id});
    // sendbird 연결
    sb.connect(user_id, function(user, error) {
        if (error) {
            return;
        }
    });
       
    // ChannelHandler 객체
     var ChannelHandler = new sb.ChannelHandler();

     //초대 받은 경우
     ChannelHandler.onUserJoined = function(groupChannel, user) {
        location.reload();
     };

    // 메시지 받기
    ChannelHandler.onMessageReceived = function(channel, message){
     location.reload();
    };

    sb.addChannelHandler('recieve_id2_ChannelHandlerIdTmp', ChannelHandler);
  

}

function init_detail(application_id, channel_url, user_id){
    var sb = new SendBird({appId: application_id});
    // sendbird 연결
    sb.connect(user_id, function(user, error) {
        if (error) {
            return;
        }
    });

  sb.GroupChannel.getChannel(channel_url, function(groupChannel, error) {
        if (error) {
              return;
        }

        // ChannelHandler 객체
        var ChannelHandler = new sb.ChannelHandler();

  

          // 메시지 받기
          ChannelHandler.onMessageReceived = function(channel, message){
            if(channel_url == channel.url){
                let sender_nickname = message.sender.nickname
                let sent_message = message.message
                let receive_time = message.createdAt
                
                let get_div = document.getElementById("new_message");
                var Mdiv = document.createElement('div');
                Mdiv.className = 'message';
                get_div.append(Mdiv);
                var img = document.createElement("img");
                img.src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg";
                Mdiv.appendChild(img);
                var nick = document.createElement('div');
                nick.className = 'nickname';
                nick.innerText = sender_nickname;
                Mdiv.appendChild(nick);
                var Bdiv = document.createElement('div');
                Bdiv.className = 'bubble';
                Bdiv.innerText = sent_message;
                Mdiv.appendChild(Bdiv);
                var Cdiv = document.createElement('div');
                Cdiv.className = 'corner';
                Bdiv.appendChild(Cdiv);
                Tspan = document.createElement('span');
                Tspan.innerText = change_time(receive_time);
                Bdiv.appendChild(Tspan);
  
                scrollDown();



            }
             
        };

        sb.addChannelHandler('test_id2_ChannelHandlerIdTmp', ChannelHandler);


        // 메시지 발송 객체 함수 할당
        sendMsgObj = function (msg) {
              groupChannel.sendUserMessage(msg, groupChannel.data, groupChannel.customType, function(message, error){
              if (error) {
                    return;
              }
              let sent_message = message.message
              let receive_time = message.createdAt

              $('#tx_send').val("");
              let get_div = document.getElementById("new_message");
              var Mdiv = document.createElement('div');
              Mdiv.className = 'message right';
              get_div.append(Mdiv);
              var Bdiv = document.createElement('div');
              Bdiv.className = 'bubble';
              Bdiv.innerHTML = sent_message;
              Mdiv.appendChild(Bdiv);
              var Cdiv = document.createElement('div');
              Cdiv.className = 'corner';
              Bdiv.appendChild(Cdiv);
              Tspan = document.createElement('span');
              Tspan.innerText = change_time(receive_time);
              Bdiv.appendChild(Tspan);

               scrollDown();
              });
        }
  });
    



}



function send_message(){
    sendMsgObj($('#tx_send').val());
    return false; 
}


$(function() {
$('textarea').on('keydown', function(event) {
    if (event.keyCode == 13)
        if (!event.shiftKey){
           
            send_message();

        }

})});
