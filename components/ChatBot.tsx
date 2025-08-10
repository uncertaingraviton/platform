import { useState } from 'react'
import { Send } from 'lucide-react'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

export function ChatBot() {
  const [message, setMessage] = useState('')

  const handleSendMessage = () => {
    if (message.trim()) {
      // Handle message sending logic here
      console.log('Sending message:', message)
      setMessage('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage()
    }
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 sm:bottom-6 sm:left-6 sm:right-6 z-[100]">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white border-2 border-gray-200 rounded-2xl shadow-lg backdrop-blur-sm p-3 sm:p-4">
          <div className="flex gap-2 sm:gap-3">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 text-sm sm:text-base border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0"
            />
            <Button
              onClick={handleSendMessage}
              disabled={!message.trim()}
              className="shrink-0 w-9 h-9 sm:w-10 sm:h-10 p-0 rounded-xl bg-gray-900 hover:bg-gray-800"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
