// Initialize CodeMirror
const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'text/x-c++src',
    theme: 'monokai',
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true,
    extraKeys: {"Ctrl-Space": "autocomplete"}
});

// Chat functionality
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

// Configure marked options
marked.setOptions({
    breaks: true, // Convert line breaks to <br>
    gfm: true,    // GitHub Flavored Markdown
    headerIds: false, // Disable header IDs for security
    mangle: false,    // Disable header ID mangling
    sanitize: false   // Allow HTML tags
});

function formatMessage(message) {
    // First, handle code blocks
    const parts = message.split(/```(\w*)\n([\s\S]*?)```/);
    const formattedParts = [];

    for (let i = 0; i < parts.length; i++) {
        if (i % 3 === 0) {
            // Regular text - parse as markdown
            const markdownHtml = marked.parse(parts[i]);
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = markdownHtml;
            formattedParts.push(tempDiv);
        } else if (i % 3 === 1) {
            // Language identifier (if any)
            const language = parts[i];
            const code = parts[i + 1];
            const codeBlock = document.createElement('div');
            codeBlock.className = 'code-block';
            if (language) {
                codeBlock.setAttribute('data-language', language);
            }
            codeBlock.textContent = code;
            formattedParts.push(codeBlock);
            i++; // Skip the next part as we've already used it
        }
    }

    return formattedParts;
}

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    
    if (isUser) {
        messageDiv.textContent = content;
    } else {
        const markdownContent = document.createElement('div');
        markdownContent.className = 'markdown-content';
        markdownContent.innerHTML = marked.parse(content);
        messageDiv.appendChild(markdownContent);
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    const code = codeEditor.getValue().trim();
    
    if (!message && !code) return;

    // Prepare the message to send
    let fullMessage = message;
    if (code) {
        fullMessage += (message ? '\n\n' : '') + '```cpp\n' + code + '\n```';
    }

    // Add the message to chat
    addMessage(fullMessage, true);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: fullMessage }),
        });

        const data = await response.json();
        if (data.error) {
            addMessage('Error: ' + data.error);
        } else {
            addMessage(data.response);
        }
    } catch (error) {
        addMessage('Error al comunicarse con el servidor');
    }
}); 