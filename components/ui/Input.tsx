import * as React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", ...props }, ref) => (
    <input
      ref={ref}
      className={`block w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm shadow-sm placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500/20 disabled:opacity-50 ${className}`}
      {...props}
    />
  )
);
Input.displayName = "Input";
