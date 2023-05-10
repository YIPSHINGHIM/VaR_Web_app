import React, { useEffect, useState } from "react";
const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const body = document.body;
    isOpen
      ? (body.style.overflow = "hidden")
      : (body.style.overflow = "visible");
  }, [isOpen]);

  return (
    <nav className="bg-gray-100 p-2 shadow-md">
      <div className="container mx-auto flex items-center justify-between">
        <a href="/" className="text-3xl font-medium">
          Value at Risk
        </a>
        <div className={`${isOpen ? "block" : "hidden"} sm:flex`}>
          <a
            href="/"
            className="px-4 py-2 mr-4 text-gray-800 hover:text-gray-600"
          >
            Home
          </a>
          <a
            href="#/VarDifferentMethod"
            className="px-4 py-2 mr-4 text-gray-800 hover:text-gray-600"
          >
            Var Different Method
          </a>
          <a
            href="#/VarWithOption"
            className="px-4 py-2 text-gray-800 hover:text-gray-600"
          >
            Var With Option
          </a>
        </div>
        <div className="sm:hidden">
          <button
            className="px-3 py-2 border border-gray-400 rounded-lg hover:bg-gray-200"
            onClick={() => setIsOpen(!isOpen)}
          >
            Menu
          </button>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
