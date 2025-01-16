// Wait for the window to load
window.addEventListener('load', function () {
    // Get the pre-loader and navbar elements
    var preloader = document.getElementById('preloader');
    var navbar = document.querySelector('.navbar');

    // Hide the navbar initially
    navbar.style.display = 'none';

    // Hide the pre-loader and show the navbar after a delay
    setTimeout(function() {
        preloader.style.opacity = '0'; // Fade out the pre-loader
        setTimeout(function() {
            preloader.style.zIndex = '0'; // Set z-index to 0 after fade-out
            preloader.style.opacity = '0'; // Set opacity to 0 after fade-out
            setTimeout(function() {
                preloader.style.display = 'none'; // Hide the pre-loader completely after fade-out and opacity/z-index set to 0
                navbar.style.display = 'block'; // Show the navbar
            }, .01); // Wait for 1 second after fade-out before hiding pre-loader
        }, 1000); // Wait for 1 second after fade-out before setting opacity/z-index to 0
    }, 2500); // Adjust the delay (in milliseconds) according to your video duration
});





// CHATBOT

const sendChatBtn = document.querySelector(".chat-input span");
const chatInput = document.querySelector(".chat-input textarea");
const chatBox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");
let userMessage;
const inputHeight = chatInput.style.scrollHeight;

const createChatLi = (message, className) =>{
    const chatLi = document.createElement("Li");
    chatLi.classList.add("chat", className);
    let chatContent = className === 'outgoing' ? `<p></p>` : `<span class="fa-solid fa-robot"></span>
    <p></p>`
    // <span class="fa-solid fa-user" id="user-icon"></span>

    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

const handleChat = () =>{
    userMessage = chatInput.value;
    if(!userMessage) return;
    chatInput.value = "";

    chatBox.append(createChatLi(userMessage, 'outgoing'));
    chatBox.scrollTo(0, chatBox.scrollHeight);
    setTimeout(()=>{
        const incomingChatLi = createChatLi('Thinking......', 'incoming');
        chatBox.append(incomingChatLi);
        chatBox.scrollTo(0, chatBox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

sendChatBtn.onclick = () => {
    handleChat();
}


// Animation
chatbotToggler.onclick = () => {
    document.body.classList.toggle('show-chatbot');
}

chatbotCloseBtn.onclick = () => {
    document.body.classList.remove('show-chatbot');
}

chatInput.oninput = () => {
    chatInput.style.height = `${inputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
}

chatInput.onkeydown = (e) => {
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth>800){
        e.preventDefault();
        handleChat();
    }
}


// The frontend will send the user’s input to the Flask backend and receive the relevant sloka in response.
const generateResponse = async (incomingChatLi) => {
    try {
        const response = await fetch('http://127.0.0.1:5001', {  // Correct backend URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: userMessage })  // Ensure userMessage is not empty
        });
        

        const data = await response.json();
        const { emotion, verse } = data;

        // Update the chatbot with the received verse and emotion
        incomingChatLi.querySelector('p').textContent = `Emotion: ${emotion} \nSloka: ${verse.Shoka}\nMeaning: ${verse.EngMeaning}`;
        chatBox.scrollTo(0, chatBox.scrollHeight);
    } catch (error) {
        incomingChatLi.querySelector('p').textContent = 'Sorry, there was an error. Please try again.';
    }
};

fetch('http://127.0.0.1:5001/', {
    method: 'POST',
    mode: 'cors', // Explicitly enable CORS
    body: JSON.stringify({ message: userMessage }),
    headers: { 'Content-Type': 'application/json' },
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log(data);
})
.catch(error => {
    console.error('Error:', error);
});
