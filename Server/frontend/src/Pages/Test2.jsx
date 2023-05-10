import React, { useEffect, useState } from "react";
import GaugeChart from "react-gauge-chart";
import SideBar from "../components/SideBar";

const VarDifferentMethod = () => {
  // for the sideBar
  const [ticket, setTicket] = useState([]);
  const [weight, setWeight] = useState([]);
  const [Input, setInput] = useState({});
  const [data, setData] = useState(null);
  const [statusCode, setStatusCode] = useState(null);

  const handleFormSubmit = (values) => {
    setTicket(values);
  };

  const handleFormSubmit2 = (values) => {
    setWeight(values);
  };

  const handleFormSubmit3 = (inputs) => {
    setInput(inputs);
  };

  const resetInput = () => {
    setTicket([]);
    setWeight([]);
    setInput({});
  };

  let tempInput = { ...Input };

  if (ticket.length > 0 && weight.length > 0) {
    if (ticket.length === weight.length) {
      tempInput["stock_list"] = ticket.toString();
      tempInput["portfolio_weights"] = weight.toString();
    } else {
      alert(
        "Given the wrong output , the number of ticket and the number of weight is not match please enter again "
      );
      resetInput();
    }
  }

  const handleButtonClick = async () => {
    // This is accepting the data
    const response = await fetch("http://127.0.0.1:5000/api/get_data_view", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tempInput),
    });
    setStatusCode(response.status);
    const json = await response.json();
    setData(json);
  };

  // For the simulation
  const [dataHS, setDataHS] = useState(null);
  const [dataMB, setDataMB] = useState(null);
  const [dataMS, setDataMS] = useState(null);

  useEffect(() => {
    const putData = async () => {
      const RequestHS = await fetch("http://127.0.0.1:5000/api/simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          method: "hs",
        }),
      });
      const HSVaRObj = await RequestHS.json();

      const RequestMB = await fetch("http://127.0.0.1:5000/api/simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          method: "mb_1",
        }),
      });
      const MBVaRObj = await RequestMB.json();

      const RequestMS = await fetch("http://127.0.0.1:5000/api/simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          method: "ms_1",
        }),
      });
      const MSVaRObj = await RequestMS.json();

      setDataHS(HSVaRObj);
      setDataMB(MBVaRObj);
      setDataMS(MSVaRObj);
    };
    putData().catch((error) => console.error(error));
  }, []);

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

  // selection box for choosing different method the calculated the VaR
  const [selectedMBMethod, setSelectedMBMethod] = useState("mb_1");
  const [selectedMSMethod, setSelectedMSMethod] = useState("ms_1");

  useEffect(() => {
    if (selectedMBMethod) {
      const fetchData = async () => {
        const response = await fetch("http://127.0.0.1:5000/api/simulation", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            method: selectedMBMethod,
          }),
        });
        const MBNewData = await response.json();
        setDataMB(MBNewData);
      };
      fetchData();
    }
  }, [selectedMBMethod]);

  const handleMBMethodChange = (event) => {
    setSelectedMBMethod(event.target.value);
  };

  useEffect(() => {
    if (selectedMSMethod) {
      const fetchData = async () => {
        const response = await fetch("http://127.0.0.1:5000/api/simulation", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            method: selectedMSMethod,
          }),
        });
        const MSNewData = await response.json();
        setDataMS(MSNewData);
      };
      fetchData();
    }
  }, [selectedMSMethod]);

  const handleMSMethodChange = (event) => {
    setSelectedMSMethod(event.target.value);
  };

  return (
    <div className="VarDifferentMethod">
      <div className="grid grid-cols-12 grid-row-2 gap-1">
        <div className="left col-span-2">
          <SideBar
            ticket={ticket}
            weight={weight}
            Input={Input}
            handleFormSubmit={handleFormSubmit}
            handleFormSubmit2={handleFormSubmit2}
            handleFormSubmit3={handleFormSubmit3}
            handleButtonClick={handleButtonClick}
            data={data}
          />
        </div>

        <div className="right col-span-10">
          <h2>This is VAR Different Method</h2>
          {dataHS && dataMB && dataMS ? (
            <div className="grid grid-cols-3">
              <div className="historical bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">Historical Simulation</h2>

                <br />

                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment}
                </h2>
                <h2 className="text-2xl">
                  Value at Risk 95th : ${HSVaR.toFixed(4)}
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

              <div className="module_build  bg-gray-100 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  module build Simulation
                </h2>
                <br />
                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment2}
                </h2>
                <h2 className="text-2xl">
                  Value at Risk 95th : {MBVaR.toFixed(4)}
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

              <div className="Monte_Carlo_Simulation bg-gray-200 mx-3 rounded-md">
                <h2 className="text-3xl text-sky-400">
                  Monte Carlo Simulation
                </h2>
                <br />
                <h2 className="text-2xl">
                  Initial Investment : ${InitialInvestment3}
                </h2>
                <h2 className="text-2xl">
                  Value at Risk 95th : {MSVaR.toFixed(4)}
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
            </div>
          ) : (
            <p className=" text-3xl font-bold">Loading data...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default VarDifferentMethod;
