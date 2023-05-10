import React, { useState } from "react";
import SideBar from "../components/SideBar";
import TimeSeriesGraph from "../components/TimeSeriesGraph";

const Test = () => {
  const [ticket, setTicket] = useState([]);
  const [weight, setWeight] = useState([]);
  const [Input, setInput] = useState({});
  const [data, setData] = useState(null);
  const [statusCode, setStatusCode] = useState(null);
  const [closingPriceData, setClosingPriceData] = useState(null);
  const [returnData, setReturnData] = useState(null);

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
    // console.log(tempInput);
    // console.log({
    //   type: "ClosingPrice",
    // });

    console.log(tempInput);

    // TODO can be refactor , make the function to fetch two api in the same time using the await Promise.all
    // This is getting the closing price
    if (statusCode === 200) {
      const closingPriceResponse = await fetch(
        "http://127.0.0.1:5000/api/graph_data",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            type: "ClosingPrice",
          }),
        }
      );
      const closingPriceJson = await closingPriceResponse.json();
      const tempClosingPriceObj = JSON.parse(closingPriceJson);
      setClosingPriceData(tempClosingPriceObj);

      const ReturnResponse = await fetch(
        "http://127.0.0.1:5000/api/graph_data",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            type: "Return",
          }),
        }
      );
      const ReturnJson = await ReturnResponse.json();
      const tempReturnObj = JSON.parse(ReturnJson);
      setReturnData(tempReturnObj);
    }
  };
  console.log(closingPriceData);

  return (
    <div className="Home">
      <div className="grid grid-cols-12 grid-row-2 gap-1">
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
        <div className="right col-span-10">
          <div className="row-start-1">
            <TimeSeriesGraph
              data={closingPriceData}
              title="Compare closing price"
            />
          </div>

          <div className="row-end-1">
            <TimeSeriesGraph data={returnData} title="Compare Return" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Test;
