export const BasketballLogo = () => {
  return (
    <svg
      width="40"
      height="40"
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="text-foreground"
    >
      {/* Main circle */}
      <circle
        cx="50"
        cy="50"
        r="48"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Left arc */}
      <path
        d="M 18 15 Q 10 50 18 85"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Right arc */}
      <path
        d="M 82 15 Q 90 50 82 85"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Top horizontal arc */}
      <path
        d="M 15 18 Q 50 10 85 18"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Bottom horizontal arc */}
      <path
        d="M 15 82 Q 50 90 85 82"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Diagonal top-left to bottom-right */}
      <path
        d="M 20 20 Q 50 50 80 80"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
      
      {/* Diagonal top-right to bottom-left */}
      <path
        d="M 80 20 Q 50 50 20 80"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
      />
    </svg>
  );
};
