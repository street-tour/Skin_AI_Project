$(document).ready(function() {
    const chatbotToggler = $('.chatbot-toggler');
    const chatbox = $(".chatbox");
    const chatInput = $(".chat-input textarea");
    const sendChatBtn = $(".chat-input span");

    chatbotToggler.on('click', () => $('body').toggleClass('show-chatbot'));

    sendChatBtn.on("click", function() {
        const message = chatInput.val();
        if (message.trim() === "") return;

        chatbox.append(`<li class="chat outgoing"><p>${message}</p></li>`);
        chatInput.val("");
        chatbox.scrollTop(chatbox[0].scrollHeight);
        
        const botResponse = `<li class="chat incoming"><span class="material-symbols-outlined">smart_toy</span><p>Thinking...</p></li>`;
        chatbox.append(botResponse);

        fetch("/chatbot/chat-text-with-custom-info2/", {
            method: "POST",
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body: JSON.stringify({"message": message})
        })
        .then(resp => resp.json())
        .then(data => {
            chatbox.find(".incoming p").last().text(data.message);
            chatbox.scrollTop(chatbox[0].scrollHeight);
        });
    });

    chatInput.on("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendChatBtn.click();
        }
    });
});