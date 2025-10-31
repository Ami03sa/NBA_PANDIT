import React from "react";

export const BasketballLogo = () => (
  <div className="flex items-center justify-center bg-black p-4 rounded-lg">
    {/* Two vertical white bars (like HH logo) */}
    <div className="flex space-x-1 mr-3">
      <div className="bg-white w-2 h-12 rounded-sm"></div>
      <div className="bg-white w-2 h-12 rounded-sm"></div>
    </div>

    {/* BALLTALK Text */}
    <div className="flex flex-col leading-none text-white font-extrabold text-4xl tracking-tight">
      <span>BALL</span>
      <span>TALK</span>
    </div>
  </div>
);
