import { useState, useRef, useEffect } from 'react'
import { Send, Target, Info } from 'lucide-react'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

interface Message {
  id: number
  text: string
  isUser: boolean
  timestamp: Date
  isSolution?: boolean
}

interface Problem {
  id: string
  title: string
  description: string
  difficulty_level: string
  category: string
  total_steps: number
}

export function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isHistoryCollapsed, setIsHistoryCollapsed] = useState(true)
  const [currentProblem, setCurrentProblem] = useState<Problem | null>(null)
  const chatRef = useRef<HTMLDivElement>(null)

  // Load current problem on component mount
  useEffect(() => {
    loadCurrentProblem()
  }, [])

  const loadCurrentProblem = async () => {
    try {
      const response = await fetch('http://localhost:8000/problem/current')
      if (response.ok) {
        const data = await response.json()
        setCurrentProblem(data)
        
        // Add welcome message
        const welcomeMessage: Message = {
          id: Date.now(),
          text: `🎯 Welcome! The current problem is:\n\n📝 ${data.title}\n\n${data.description}\n\nType your solution and I'll evaluate it!`,
          isUser: false,
          timestamp: new Date()
        }
        setMessages([welcomeMessage])
      }
    } catch (error) {
      console.error('Error loading current problem:', error)
      // Add error message
      const errorMessage: Message = {
        id: Date.now(),
        text: 'Unable to load the current problem. Please try refreshing the page.',
        isUser: false,
        timestamp: new Date()
      }
      setMessages([errorMessage])
    }
  }

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
      timestamp: new Date(),
      isSolution: true
    }

    setMessages(prev => [...prev, userMessage])
    setMessage('')
    setIsLoading(true)

    // Auto-expand history when sending a message
    setIsHistoryCollapsed(false)

    try {
      const requestBody = {
        user_input: message
      }

      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
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
        timestamp: new Date(),
        isSolution: true
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
        timestamp: new Date()
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

  const showProblemInfo = async () => {
    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: "show problem" }),
      })

      if (response.ok) {
        const reader = response.body?.getReader()
        if (!reader) return

        let problemInfo = ''
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          problemInfo += new TextDecoder().decode(value)
        }

        // Add problem info message
        const infoMessage: Message = {
          id: Date.now(),
          text: problemInfo,
          isUser: false,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, infoMessage])
        setIsHistoryCollapsed(false)
      }
    } catch (error) {
      console.error('Error getting problem info:', error)
    }
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 sm:bottom-6 sm:left-6 sm:right-6 z-[100]">
      <div className="max-w-4xl mx-auto">
        <div ref={chatRef} className="bg-white border-2 border-gray-200 rounded-2xl shadow-lg backdrop-blur-sm">
          {/* Current Problem Status */}
          {currentProblem && (
            <div className="p-4 border-b-2 border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <Target className="w-5 h-5 text-blue-600" />
                  {currentProblem.title}
                </h3>
                <Button
                  onClick={showProblemInfo}
                  className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-1"
                >
                  <Info className="w-4 h-4" />
                  Problem Info
                </Button>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-700">
                    {currentProblem.description}
                  </span>
                </div>
              </div>
              
              <div className="flex gap-2 mt-2">
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                  {currentProblem.difficulty_level}
                </span>
                <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
                  {currentProblem.category}
                </span>
              </div>
            </div>
          )}

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
                        } ${msg.isSolution ? 'border-l-4 border-blue-500' : ''}`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
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
                placeholder="Type your solution here..."
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
