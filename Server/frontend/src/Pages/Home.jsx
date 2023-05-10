import React, { useState } from "react";
import StockVaRSideBar from "../components/StockVaRSideBar";
import TimeSeriesGraph from "../components/TimeSeriesGraph";
// import OptionVaRSideBar from "../components/OptionVaRSideBar";

const Home = () => {
  const [userInput, setUserInput] = useState({});
  const [checkResult, setCheckResult] = useState(null);
  const [closingPriceData, setClosingPriceData] = useState(null);
  const [returnData, setReturnData] = useState(null);

  const sendInputToApi = async (inputData, apiUrl, setFunc) => {
    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
      });

      if (response.ok) {
        const jsonResponse = await response.json();
        console.log("API response:", jsonResponse);
        const tempObj = JSON.stringify(jsonResponse, null, 2);
        if (tempObj === "true") {
          setFunc(true);
        } else if (tempObj === "False") {
          setFunc(false);
        } else {
          setFunc(jsonResponse);
        }
      } else {
        throw new Error(`Request failed with status ${response.status}`);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleStockVaRSubmit = (data) => {
    setUserInput(data);
    console.log(data);

    sessionStorage.setItem("stockKey", JSON.stringify(data));

    const apiUrl = "http://127.0.0.1:5000/api/get_data_view";
    sendInputToApi(data, apiUrl, setCheckResult);
    console.log(checkResult);

    // closingPriceResponse
    const closingPriceResponseUrl = "http://127.0.0.1:5000/api/graph_data";
    sendInputToApi(
      {
        type: "ClosingPrice",
      },
      closingPriceResponseUrl,
      setClosingPriceData
    );
    console.log(closingPriceData);

    // ReturnResponse
    const ReturnResponseUrl = "http://127.0.0.1:5000/api/graph_data";
    sendInputToApi(
      {
        type: "Return",
      },
      ReturnResponseUrl,
      setReturnData
    );
    console.log(returnData);
  };

  return (
    <div className="flex">
      <div className="w-1/5">
        <StockVaRSideBar onSubmit={handleStockVaRSubmit} />
      </div>

      <div className="w-4/5">
        <div className="ml-4">
          {!checkResult && (
            <h1 className="text-4xl font-semibold text-red-500">
              Input the information to see the Graph !
            </h1>
          )}
          <TimeSeriesGraph
            data={JSON.parse(closingPriceData, null, 2)}
            title="Compare closing price"
          />

          <TimeSeriesGraph
            data={JSON.parse(returnData, null, 2)}
            title="Compare Return"
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
