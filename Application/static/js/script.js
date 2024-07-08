const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const id=document.querySelector('.hidden').textContent;
let userText = null;
const loadDataFromLocalstorage = () => {
  // Load saved chats and theme from local storage and apply/add on the page
  const themeColor = localStorage.getItem("themeColor");
  
  document.body.classList.toggle("light-mode", themeColor === "light_mode");
  themeButton.innerText = document.body.classList.contains("light-mode")
    ? "dark_mode"
    : "light_mode";

  const defaultText = `<div class="default-text">
                            <h1>Mental Health ChatBot</h1>
                            <p>Start a conversation with our chatbot.<br> Your chat history is saved and can be deleted.</p>
                        </div>`;

  chatContainer.innerHTML = localStorage.getItem(id) || defaultText;
  console.log(chatContainer.in)
  chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to bottom of the chat container
};

const createChatElement = (content, className) => {
  // Create new div and apply chat, specified class and set html content of div
  const chatDiv = document.createElement("div");
  chatDiv.classList.add("chat", className);
  chatDiv.innerHTML = content;
  return chatDiv; // Return the created chat div
};

const getChatResponse = async (incomingChatDiv,userText) => {
  const pElement = document.createElement("p");
  // Send POST request to API, get response and set the reponse as paragraph element text
  try {
    const response = await fetch('/chat',{
      method:'POST',
      headers:{
             "Content-Type": "application/json",
      },
      body:JSON.stringify(
        {
          'userText':userText,
          'userID':id
        }
      )
    });
    const data=await response.json()
    pElement.textContent = data.message.trim();
  } catch (error) {
    console.error(error)
    pElement.classList.add("error");
    pElement.textContent =
      "Oops! Something went wrong while retrieving the response. Please try again.";
  }

  // Remove the typing animation, append the paragraph element and save the chats to local storage
  incomingChatDiv.querySelector(".typing-animation").remove();
  incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
  localStorage.setItem(id, chatContainer.innerHTML);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

// const copyResponse = (copyBtn) => {
//   // Copy the text content of the response to the clipboard
//   const reponseTextElement = copyBtn.parentElement.querySelector("p");
//   navigator.clipboard.writeText(reponseTextElement.textContent);
//   copyBtn.textContent = "done";
//   setTimeout(() => (copyBtn.textContent = "content_copy"), 1000);
// };

const showTypingAnimation = (userText) => {
  // Display the typing animation and call the getChatResponse function
  const html = `
    <div class="chat-content">
      <div class="chat-details">
      <img src="static/images/AI.png" alt="chatbot-img" >
        <div class="typing-animation">
          <div class="typing-dot" style="--delay: 0.2s"></div>
          <div class="typing-dot" style="--delay: 0.3s"></div>
          <div class="typing-dot" style="--delay: 0.4s"></div>
        </div>
      </div>
    </div>
  `;
  // Create an incoming chat div with typing animation and append it to chat container
  const incomingChatDiv = createChatElement(html, "incoming");
  chatContainer.appendChild(incomingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  getChatResponse(incomingChatDiv,userText);
};

const handleOutgoingChat = () => {
  userText = chatInput.value.trim(); // Get chatInput value and remove extra spaces
  if (!userText) return; // If chatInput is empty return from here
  // Clear the input field and reset its height
  chatInput.value = "";
  chatInput.style.height = `${initialInputHeight}px`;

  const html = `
    <div class="chat-content">
      <div class="chat-details">
        <img src="static/images/user.png" alt="user-img" >
        <p>${userText}</p>
      </div>
    </div>
  `;

  // Create an outgoing chat div with user's message and append it to chat container
  const outgoingChatDiv = createChatElement(html, "outgoing");
  chatContainer.querySelector(".default-text")?.remove();
  chatContainer.appendChild(outgoingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  setTimeout(showTypingAnimation(userText), 500);
};

deleteButton.addEventListener("click", () => {
  // Remove the chats from local storage and call loadDataFromLocalstorage function
  if (confirm("Are you sure you want to delete all the chats?")) {
    localStorage.removeItem(id);
    loadDataFromLocalstorage();
  }
});

themeButton.addEventListener("click", () => {
  // Toggle body's class for the theme mode and save the updated theme to the local storage
  document.body.classList.toggle("light-mode");
  localStorage.setItem("themeColor", themeButton.innerText);
  themeButton.innerText = document.body.classList.contains("light-mode")
    ? "dark_mode"
    : "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {
  // Adjust the height of the input field dynamically based on its content
  chatInput.style.height = `${initialInputHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  // If the Enter key is pressed without Shift and the window width is larger
  // than 800 pixels, handle the outgoing chat
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleOutgoingChat();
  }
});

loadDataFromLocalstorage();
sendButton.addEventListener("click", handleOutgoingChat);
