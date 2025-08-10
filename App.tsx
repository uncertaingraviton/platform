import { Header } from "./components/Header";
import { ChatBot } from "./components/ChatBot";
import "./styles/globals.css";

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main
        className="px-4 sm:px-6 py-6 sm:py-12 pb-28 sm:pb-32"
        style={{
          backgroundImage: `
            linear-gradient(rgba(156, 163, 175, 0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(156, 163, 175, 0.15) 1px, transparent 1px)
          `,
          backgroundSize: "20px 20px",
          backgroundAttachment: "fixed",
        }}
      >
        <div className="max-w-7xl mx-auto mb-6 sm:mb-8">
          <h1
            className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl xl:text-9xl leading-tight font-bold text-gray-900"
            style={{ fontFamily: "Helvetica, sans-serif" }}
          >
            Large Heading
          </h1>
        </div>

        {/* Container that extends with content */}
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-4 sm:p-6 min-h-[60vh]">
            {/* Content will go here */}
            <div className="text-gray-600">
              Container content goes here...
            </div>

            {/* Demo content to show scrolling */}
            <div className="mt-8 space-y-4">
              {Array.from({ length: 10 }, (_, i) => (
                <div
                  key={i}
                  className="p-4 bg-gray-50 rounded-md border border-gray-100"
                >
                  <p>
                    Demo content block {i + 1} - This content
                    demonstrates scrolling behavior on the page.
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <ChatBot />
    </div>
  );
}
