import { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

interface Message {
  id: number
  text: string
  isUser: boolean
}

export function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isHistoryCollapsed, setIsHistoryCollapsed] = useState(true)
  const chatRef = useRef<HTMLDivElement>(null)

  // Handle click outside to collapse only the history
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (chatRef.current && !chatRef.current.contains(event.target as Node)) {
        setIsHistoryCollapsed(true)
      }
    }

    if (!isHistoryCollapsed) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isHistoryCollapsed])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now(),
      text: message,
      isUser: true,
    }

    setMessages(prev => [...prev, userMessage])
    setMessage('')
    setIsLoading(true)

    // Auto-expand history when sending a message
    setIsHistoryCollapsed(false)

    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('No response body')
      }

      let assistantMessage = ''
      const assistantMessageId = Date.now() + 1

      // Add initial assistant message
      setMessages(prev => [...prev, {
        id: assistantMessageId,
        text: '',
        isUser: false,
      }])

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = new TextDecoder().decode(value)
        assistantMessage += chunk

        // Update the assistant message
        setMessages(prev => prev.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, text: assistantMessage }
            : msg
        ))
      }
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message
      setMessages(prev => [...prev, {
        id: Date.now() + 2,
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleInputClick = () => {
    // Show history when clicking on input field
    if (messages.length > 0) {
      setIsHistoryCollapsed(false)
    }
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 sm:bottom-6 sm:left-6 sm:right-6 z-[100]">
      <div className="max-w-4xl mx-auto">
        <div ref={chatRef} className="bg-white border-2 border-gray-200 rounded-2xl shadow-lg backdrop-blur-sm">
          {/* Messages Display - Collapsible */}
          {messages.length > 0 && (
            <div className={`transition-all duration-300 ease-in-out overflow-hidden ${
              isHistoryCollapsed ? 'max-h-0 opacity-0' : 'max-h-64 opacity-100'
            }`}>
              <div className="p-3 sm:p-4 border-b-2 border-gray-200">
                <div className="space-y-3 max-h-48 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 pr-2">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-3 py-2 rounded-lg ${
                          msg.isUser
                            ? 'bg-gray-900 text-white'
                            : 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        <p className="text-sm">{msg.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Input Area - Always Visible */}
          <div className="p-3 sm:p-4">
            <div className="flex gap-2 sm:gap-3">
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                onClick={handleInputClick}
                placeholder="Type your message here..."
                className="flex-1 text-sm sm:text-base border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 cursor-text"
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!message.trim() || isLoading}
                className="shrink-0 w-9 h-9 sm:w-10 sm:h-10 p-0 rounded-xl bg-gray-900 hover:bg-gray-800 disabled:opacity-50"
              >
                <Send className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
