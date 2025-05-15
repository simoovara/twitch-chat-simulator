var darkMode = false;


//is called automatically when the html page is loaded
function init()
{
    // meow
}



function replaceEmotes(message)
{
    message = " " + message + " "; //add space before and after

    for (var i=0;i<emotes.length;i++)
    {
        message = message.replace(new RegExp("\\b" + emotes[i][0] + "\\b", 'g'), " <img src='index_files/assets/emotes/" + emotes[i][1] + "' alt='" + emotes[i][0] + "'> ");
    }

    message = message.slice(1, -1); //remove the added spaces
    return message;
}


//returns a random username
function getUserName()
{
    var username = $('<span></span>');
    username.attr("class", "username");
    username.css("color", getUsernameColor());
    username.append(usernamePrefixes[Math.floor(Math.random()*usernamePrefixes.length)]);   //gets a random username from the array
    username.append(usernameSuffixes[Math.floor(Math.random()*usernameSuffixes.length)]);   //gets a random username from the array

    if(Math.random() > 0.5)
    {
        username.append(Math.floor(Math.random() * 120));
    }

    return username;
}

//returns one of the colours you could have as your username
function getUsernameColor()
{
    return usernameColors[Math.floor(Math.random()*usernameColors.length)];
}


//hides the chat text
function hideChatText()
{
    var element = $("#chattext");
    var hideButton = $("#hideButton");

    element.toggle();
    hideButton.empty();

    if(element.is(":visible"))
    {
        hideButton.append("hide");
    }
    else
    {
        hideButton.append("show");
    }
}

//clears the chat of messages
function clearChat()
{
    var element = $("#chattext");

    element.empty();
}


window.chat = chat;



//writes the text of the input field into the chat with a random username
function chat(highlight, userName)
{
    var textfield = $("#textfield");
    var element = $("#chattext");

    if(textfield.val()!=="") {
        var message = $('<p></p>');
        if (highlight)
            message.attr("class", "chatMessageHighlight");
        else
            message.attr("class", "chatMessage");
        if (userName !== undefined) {
            message.append(userName.text() === "" ? getUserName() : userName);
            message.append(": ");
        }
        else {
            message.append(getUserName());
            message.append(": ");
        }

        var msgBody = textfield.val();
        msgBody = replaceEmotes(msgBody);

        message.append(msgBody);

        textfield.val("");

        element.append(message);
        scrollToBottom();
        cutTopOfChat();
    }
}

//scrolls to the bottom of the chat
function scrollToBottom()
{
    var chattext = document.getElementById("chattext");
    chattext.scrollTop = chattext.scrollHeight;
}

//checks to see if the chat is too long and cuts the top elements if it is
function cutTopOfChat()
{
    var element = $("#chattext");
    if(element.children().length > 170)
    {
        var chatMessages = element.children();
        for(i = 0; i<30; i++)
        {
            chatMessages[i].remove();
        }
    }
}


//toggles between dark mode and normal mode
function darkmode()
{
    var chat = $("#chat");
    if(darkMode)
    {
        darkMode = false;
        chat.css("color", "black");
        chat.css("background-color", "white");
        $("#textfield").css("background-color", "white");
        $("#textfield").css("color", "black");
        $("#chattext").removeAttr("class");
    }
    else
    {
        darkMode = true;
        chat.css("color", "white");
        chat.css("background-color", "#1e1e1e");
        $("#textfield").css("background-color", "#141414");
        $("#textfield").css("color", "white");
        $("#chattext").attr("class", "dark");
    }
}



//gives the user an input field to change the name of the channel
function changeChannel()
{
    $("#abovechat").empty();
    var form = $('<form></form>');
    form.attr("onsubmit", "return false");

    var input = $('<input></input>');
    input.attr("type", "text");
    input.attr("placeholder", "channel name");
    input.attr("id", "channelnameinput");

    //<input type="submit" id="videoButton" onClick="getVideo()" value="get video" onKeyPress="checkForEnter(event)">
    var button = $('<input></input>');
    button.attr("type", "submit");
    button.attr("onClick", "setChannelName()");
    button.attr("value", "set");

    form.append(input);
    form.append(button);
    $("#abovechat").append(form);
}

function setChannelName()
{
    var name = $("#channelnameinput").val();
    $("#abovechat").empty();
    var channelname = $('<p></p>');
    channelname.attr("onclick", "changeChannel()");
    channelname.attr("id", "channelname");
    channelname.append(name);
    $("#abovechat").append(channelname);
}

