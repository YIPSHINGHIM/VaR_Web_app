import React from "react";
import { createHashRouter, RouterProvider } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./Pages/Home";
import Test from "./Pages/Test";
import Test2 from "./Pages/Test2";
import VarDifferentMethod from "./Pages/VaRDifferentMethod";
import VarWithOption from "./Pages/VaRWithOption";
const router = createHashRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "Test",
    element: <Test />,
  },
  {
    path: "Test2",
    element: <Test2 />,
  },
  {
    path: "VarDifferentMethod",
    element: <VarDifferentMethod />,
  },
  {
    path: "VarWithOption",
    element: <VarWithOption />,
  },
]);

function App() {
  return (
    <div className="App">
      <div className="relative">
        <NavBar />
      </div>
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
