// Eden Agent API Integration
(async function() {
    const agentChatBox = document.getElementById('agent-chat');
    const agentInput = document.getElementById('agent-input');
    const agentSend = document.getElementById('agent-send');
    
    if (!agentChatBox || !agentInput || !agentSend) {
        return; // Agent UI elements not present on this page
    }
    
    // Check authentication status
    async function checkAuth() {
        try {
            const response = await fetch('/.auth/me');
            const data = await response.json();
            return data.clientPrincipal;
        } catch (error) {
            console.error('Auth check failed:', error);
            return null;
        }
    }
    
    // Send message to agent API
    async function sendToAgent(message) {
        try {
            const response = await fetch('/api/agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionStorage.getItem('agent_session_id') || 'default'
                })
            });
            
            if (response.status === 401) {
                return { error: 'Please log in to use the AI agent.' };
            }
            
            const data = await response.json();
            
            // Store session ID
            if (data.session_id) {
                sessionStorage.setItem('agent_session_id', data.session_id);
            }
            
            return data;
        } catch (error) {
            console.error('Agent API error:', error);
            return { error: 'Failed to connect to agent service.' };
        }
    }
    
    // Add message to chat
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `agent-message ${isUser ? 'user' : 'agent'}`;
        messageDiv.textContent = text;
        agentChatBox.appendChild(messageDiv);
        agentChatBox.scrollTop = agentChatBox.scrollHeight;
    }
    
    // Handle send button click
    agentSend.addEventListener('click', async () => {
        const message = agentInput.value.trim();
        if (!message) return;
        
        // Check auth first
        const user = await checkAuth();
        if (!user) {
            addMessage('Please log in to use the AI agent.');
            window.location.href = '/login';
            return;
        }
        
        // Add user message
        addMessage(message, true);
        agentInput.value = '';
        
        // Show loading
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'agent-message agent loading';
        loadingDiv.textContent = 'Thinking...';
        agentChatBox.appendChild(loadingDiv);
        
        // Send to API
        const result = await sendToAgent(message);
        
        // Remove loading
        agentChatBox.removeChild(loadingDiv);
        
        // Add response
        if (result.error) {
            addMessage(`Error: ${result.error}`);
        } else {
            addMessage(result.response);
        }
    });
    
    // Handle enter key
    agentInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            agentSend.click();
        }
    });
    
    // Initial greeting
    addMessage('Hello! I\'m your Eden AI agent. Ask me anything about tax, accounting, or use my calculator.');
})();
