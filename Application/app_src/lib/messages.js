import "babel-polyfill";

function removeParentElement(e) {
  e.target.parentElement.remove();
}

export function makeMessagesCloseable(){
  const messages = document.getElementsByTagName("messages")[0];
  const messageCloses = messages.getElementsByClassName("close");
  for (let i = 0; i < messageCloses.length; i++) {
    messageCloses[i].onclick = removeParentElement;
  }
}

export function makeMessage(messagetext, category){
  /* This is necessary because jQuery goes insane when used here.
   * It makes two nodes, one of which is not in the DOM. 0/10
   */
  const messageWrapper = document.createElement("div");
  messageWrapper.setAttribute("class", "message-wrapper message-" + category);
  const messageCategory = document.createElement("div");
  messageCategory.setAttribute("class", "message-category");
  messageCategory.textContent = category;
  const messageText = document.createElement("div");
  messageText.setAttribute("class", "message-text");
  messageText.textContent = messagetext;
  const closeButton = document.createElement("button");
  closeButton.setAttribute("class", "close fa fa-times-circle");
  closeButton.setAttribute("type", "button");
  closeButton.onclick = removeParentElement;
  messageWrapper.appendChild(messageCategory);
  messageWrapper.appendChild(messageText);
  messageWrapper.appendChild(closeButton);
  document.getElementsByTagName("messages")[0].appendChild(messageWrapper);
  return messageWrapper;
}

