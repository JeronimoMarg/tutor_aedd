document.addEventListener('DOMContentLoaded', () => {
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

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        if (isUser) {
            messageDiv.textContent = message;
        } else {
            const formattedParts = formatMessage(message);
            formattedParts.forEach(part => {
                if (part instanceof HTMLElement) {
                    messageDiv.appendChild(part);
                } else {
                    messageDiv.appendChild(document.createTextNode(part));
                }
            });
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Lo siento, hubo un error al procesar tu solicitud.');
        }
    });
}); 