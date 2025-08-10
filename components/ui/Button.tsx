import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", ...props }, ref) => (
    <button
      ref={ref}
      className={
        `inline-flex items-center justify-center rounded-md bg-gray-900 text-white font-medium px-4 py-2 text-sm shadow-sm transition-colors hover:bg-gray-800 disabled:opacity-50 disabled:pointer-events-none ${className}`
      }
      {...props}
    />
  )
);
Button.displayName = "Button";
