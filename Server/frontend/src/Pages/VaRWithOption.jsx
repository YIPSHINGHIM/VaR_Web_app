import React, { useEffect, useState } from "react";
import OptionVaRSideBar from "../components/OptionVaRSideBar";

const VaRWithOption = () => {
  const [input, setInput] = useState(null);
  const [flag, setFlag] = useState(null);
  const [HSOptionVaR, setHSOptionVaR] = useState(null);
  const [MSOptionVaR, setMSOptionVaR] = useState(null);

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
          setFunc(tempObj);
        }
      } else {
        throw new Error(`Request failed with status ${response.status}`);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleFormSubmit = (inputs) => {
    console.log(inputs); // You can log the inputs to the console to check them as well.
    setInput(JSON.stringify(inputs, null, 2));

    // Replace this URL with the actual API endpoint you want to send the PUT request to
    const apiUrl = "http://127.0.0.1:5000/api/option_data";
    sendInputToApi(inputs, apiUrl, setFlag);
    console.log(flag);
  };

  useEffect(() => {
    if (flag) {
      sessionStorage.setItem("key", input);
    }
  }, [flag, input]);

  let after_check_data = JSON.parse(sessionStorage.getItem("key"));
  console.log(after_check_data);

  let confidenceLevel = null;
  if (after_check_data) {
    confidenceLevel = 100 - Number(after_check_data.confidence_level);
  }

  useEffect(() => {
    if (after_check_data) {
      setInput(JSON.stringify(after_check_data, null, 2));
    }
  }, [after_check_data]);

  useEffect(() => {
    if (flag) {
      const apiUrl = "http://127.0.0.1:5000/api/option_var";

      const after_check_data_hs = { ...after_check_data, ["method"]: "hs" };
      sendInputToApi(after_check_data_hs, apiUrl, setHSOptionVaR);

      const after_check_data_ms = { ...after_check_data, ["method"]: "ms" };
      sendInputToApi(after_check_data_ms, apiUrl, setMSOptionVaR);

      setFlag(false);
    }
  }, [flag, after_check_data]);

  console.log(after_check_data);
  // console.log(typeof after_check_data);

  useEffect(() => {
    if (after_check_data) {
      const apiUrl = "http://127.0.0.1:5000/api/option_var";

      const after_check_data_hs = { ...after_check_data, ["method"]: "hs" };
      sendInputToApi(after_check_data_hs, apiUrl, setHSOptionVaR);

      const after_check_data_ms = { ...after_check_data, ["method"]: "ms" };
      sendInputToApi(after_check_data_ms, apiUrl, setMSOptionVaR);

      // setInput(after_check_data);
      setFlag(false);
    }
  }, []);

  console.log(typeof HSOptionVaR);
  console.log(HSOptionVaR);
  return (
    <div className="VaRwithOption">
      <div className="flex">
        <div className="w-1/4">
          <OptionVaRSideBar onSubmit={handleFormSubmit} />
        </div>
        <div className="w-3/4 p-4">
          <h1 className="text-4xl mb-4">VaR with Option</h1>

          {input ? (
            <div>
              <h2 className="text-2xl">Input :</h2>
              <p className=" text-xl ">
                {Object.entries(JSON.parse(input)).map(([key, value]) => (
                  <p>
                    {key}: {value}
                  </p>
                ))}
              </p>
            </div>
          ) : (
            <h2 className="text-2xl">Input : Nothing</h2>
          )}

          <div className="grid grid-cols-3">
            {HSOptionVaR ? (
              <div className="historical bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">Historical Simulation</h2>
                <h2 className="text-2xl">
                  VaR {confidenceLevel && confidenceLevel}th : $
                  {parseFloat(HSOptionVaR).toFixed(4)}
                </h2>

                <br />
                <br />
              </div>
            ) : (
              <>
                <p className=" text-3xl font-bold">Historical Simulation : </p>
                <p className=" text-3xl font-bold">Waiting for input</p>
                <br />
              </>
            )}

            {MSOptionVaR ? (
              <div className="historical bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  Monte Carlo Simulation
                </h2>

                <h2 className="text-2xl">
                  VaR {confidenceLevel && confidenceLevel}th : $
                  {parseFloat(MSOptionVaR).toFixed(4)}
                </h2>

                <br />
                <br />
              </div>
            ) : (
              <>
                <p className=" text-3xl font-bold">Monte Carlo Simulation : </p>
                <p className=" text-3xl font-bold">Waiting for input</p>
                <br />
              </>
            )}
          </div>

          {/* <h2>HS Option VaR</h2>
          {HSOptionVaR && (
            <div>
              <pre>{HSOptionVaR}</pre>
            </div>
          )}
          <h2>MS Option VaR</h2>
          {MSOptionVaR && (
            <div>
              <pre>{MSOptionVaR}</pre>
            </div>
          )} */}
        </div>
      </div>
    </div>
  );
};

export default VaRWithOption;
