import React, { useEffect, useState } from "react";
import GaugeChart from "react-gauge-chart";
import StockVaRSideBar from "../components/StockVaRSideBar";

const VarDifferentMethod = () => {
  const [userInput, setUserInput] = useState({});
  const [checkResult, setCheckResult] = useState(null);
  const [selectedMBMethod, setSelectedMBMethod] = useState("mb_1");
  const [selectedMSMethod, setSelectedMSMethod] = useState("ms_1");
  const [dataHS, setDataHS] = useState(null);
  const [dataMB, setDataMB] = useState(null);
  const [dataMS, setDataMS] = useState(null);

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

    const apiUrl = "http://127.0.0.1:5000/api/get_data_view";
    sendInputToApi(data, apiUrl, setCheckResult);
    console.log(checkResult);

    // HS method
    const HSUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: "hs",
      },
      HSUrl,
      setDataHS
    );
    // console.log(dataHS);

    // MB method
    const MBUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: selectedMBMethod,
      },
      MBUrl,
      setDataMB
    );
    // console.log(dataMB);

    //   MS method
    const MSUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: selectedMSMethod,
      },
      MSUrl,
      setDataMS
    );
    // console.log(dataMS);
  };

  useEffect(() => {
    const HSUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: "hs",
      },
      HSUrl,
      setDataHS
    );
    // console.log(dataHS);

    // MB method
    const MBUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: selectedMBMethod,
      },
      MBUrl,
      setDataMB
    );
    // console.log(dataMB);

    //   MS method
    const MSUrl = "http://127.0.0.1:5000/api/simulation";
    sendInputToApi(
      {
        method: selectedMSMethod,
      },
      MSUrl,
      setDataMS
    );
    // console.log(dataMS);
  }, [selectedMBMethod, selectedMSMethod]);

  const {
    hVaR: HSVaR,
    hCVaR: HSCVaR,
    InitialInvestment: InitialInvestment,
  } = dataHS || {};
  const { hVaR: MBVaR, InitialInvestment: InitialInvestment2 } = dataMB || {};
  const {
    hVaR: MSVaR,
    hCVaR: MSCVaR,
    InitialInvestment: InitialInvestment3,
  } = dataMS || {};

  const handleMBMethodChange = (event) => {
    setSelectedMBMethod(event.target.value);
  };

  const handleMSMethodChange = (event) => {
    setSelectedMSMethod(event.target.value);
  };
  let confidenceLevel = null;

  let data1 = sessionStorage.getItem("key");
  data1 = JSON.parse(data1);
  if (data1 === null) {
    console.log("Element does not exist in sessionStorage.");
  } else {
    console.log("Element exists in sessionStorage.");
    // confidenceLevel =
    console.log(data1);
    confidenceLevel = 100 - Number(data1.confidence_level);
  }

  return (
    <div className="flex">
      <div className="w-1/5">
        <StockVaRSideBar onSubmit={handleStockVaRSubmit} />
      </div>

      <div className="w-4/5">
        <div className="ml-4">
          <h2 className=" text-3xl">Calculating VAR using Different Method</h2>
          <div className="grid grid-cols-3">
            {dataHS ? (
              <div className="historical bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">Historical Simulation</h2>

                <br />

                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment}
                </h2>
                <h2 className="text-2xl">
                  VaR {confidenceLevel && confidenceLevel}th : $
                  {HSVaR.toFixed(4)}
                </h2>

                <br />
                <br />

                <h2 className="text-2xl">Total losing percentage : </h2>
                <br />

                <GaugeChart
                  id="gauge-chart1"
                  percent={HSVaR / InitialInvestment}
                  arcsLength={[0.1, 0.5, 0.4]}
                  textColor="#000000"
                />
              </div>
            ) : (
              <p className=" text-3xl font-bold">Loading data...</p>
            )}

            {dataMB ? (
              <div className="module_build  bg-gray-100 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  Module Build Simulation
                </h2>
                <br />
                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment2}
                </h2>
                <h2 className="text-2xl">
                  VaR {confidenceLevel && confidenceLevel}th :{" "}
                  {MBVaR.toFixed(4)}
                </h2>
                <br />

                <div className="MBMethodSelectionBox">
                  <h2>Select a Model building method:</h2>
                  <select
                    value={selectedMBMethod}
                    onChange={handleMBMethodChange}
                  >
                    <option value="">--Please choose an option--</option>
                    <option value="mb_1">MB Method 1</option>
                    <option value="mb_2">MB Method 2</option>
                  </select>
                </div>

                <h2 className="text-2xl">Total losing percentage : </h2>
                <br />

                <GaugeChart
                  id="gauge-chart1"
                  percent={MBVaR / InitialInvestment}
                  arcsLength={[0.1, 0.5, 0.4]}
                  textColor="#000000"
                />
              </div>
            ) : (
              <p className=" text-3xl font-bold">Loading data...</p>
            )}

            {dataMS ? (
              <div className="Monte_Carlo_Simulation bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  Monte Carlo Simulation
                </h2>
                <br />
                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment3}
                </h2>
                <h2 className="text-2xl">
                  VaR {confidenceLevel && confidenceLevel}th :{" "}
                  {MSVaR.toFixed(4)}
                </h2>
                <br />
                <div className="MSMethodSelectionBox">
                  <h2>Select a Monte Carlo Simulation method:</h2>
                  <select
                    value={selectedMSMethod}
                    onChange={handleMSMethodChange}
                  >
                    <option value="">--Please choose an option--</option>
                    <option value="ms_1">MS Method 1</option>
                    <option value="ms_2">MS Method 2</option>
                  </select>
                </div>

                <h2 className="text-2xl">Total losing percentage : </h2>
                <br />

                <GaugeChart
                  id="gauge-chart1"
                  percent={MSVaR / InitialInvestment}
                  arcsLength={[0.1, 0.5, 0.4]}
                  textColor="#000000"
                />
              </div>
            ) : (
              <p className=" text-3xl font-bold">Loading data...</p>
            )}
          </div>

          <h2 className=" text-3xl">Calculating CVAR using Different Method</h2>

          <div className="grid grid-cols-3">
            {dataHS ? (
              <div className="historical bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">Historical Simulation</h2>

                <br />

                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment}
                </h2>
                <h2 className="text-2xl">
                  CVaR {confidenceLevel && confidenceLevel}th : $
                  {HSCVaR.toFixed(4)}
                </h2>

                <br />
                <br />

                <h2 className="text-2xl">Total losing percentage : </h2>
                <br />

                <GaugeChart
                  id="gauge-chart1"
                  percent={HSCVaR / InitialInvestment}
                  arcsLength={[0.1, 0.5, 0.4]}
                  textColor="#000000"
                />
              </div>
            ) : (
              <p className=" text-3xl font-bold">Loading data...</p>
            )}

            {dataMS ? (
              <div className="Monte_Carlo_Simulation bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  Monte Carlo Simulation
                </h2>
                <br />
                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment3}
                </h2>
                <h2 className="text-2xl">
                  CVaR {confidenceLevel && confidenceLevel}th :{" "}
                  {MSCVaR.toFixed(4)}
                </h2>
                <br />
                <div className="MSMethodSelectionBox">
                  <h2>Select a Monte Carlo Simulation method:</h2>
                  <select
                    value={selectedMSMethod}
                    onChange={handleMSMethodChange}
                  >
                    <option value="">--Please choose an option--</option>
                    <option value="ms_1">MS Method 1</option>
                    <option value="ms_2">MS Method 2</option>
                  </select>
                </div>

                <h2 className="text-2xl">Total losing percentage : </h2>
                <br />

                <GaugeChart
                  id="gauge-chart1"
                  percent={MSCVaR / InitialInvestment}
                  arcsLength={[0.1, 0.5, 0.4]}
                  textColor="#000000"
                />
              </div>
            ) : (
              <p className=" text-3xl font-bold">Loading data...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VarDifferentMethod;