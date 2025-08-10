import { User, UserCircle, History } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/DropdownMenu"

export function Header() {
  const handleProfileClick = () => {
    console.log('Profile clicked')
    // Add profile navigation logic here
  }

  const handleHistoryClick = () => {
    console.log('History clicked')
    // Add history navigation logic here
  }

  return (
    <header className="w-full border-b-2 border-gray-200 bg-white sticky top-0 z-50 shadow-sm">
      <div className="flex items-center justify-between px-4 sm:px-6 py-3 sm:py-4">
        {/* Logo placeholder */}
        <div className="flex items-center">
          <div className="bg-gray-100 text-gray-600 px-3 sm:px-4 py-1.5 sm:py-2 rounded-md text-sm sm:text-base font-medium">
            Logo
          </div>
        </div>
        
        {/* User profile icon with dropdown */}
        <div className="flex items-center">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gray-900 rounded-full flex items-center justify-center cursor-pointer hover:opacity-80 transition-opacity">
                <User className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
              </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuItem onClick={handleProfileClick} className="cursor-pointer">
                <UserCircle className="w-4 h-4 mr-2" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleHistoryClick} className="cursor-pointer">
                <History className="w-4 h-4 mr-2" />
                History
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
