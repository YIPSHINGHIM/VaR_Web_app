import React, { useState } from "react";

const Form = ({ onFormSubmit }) => {
  const [period, setPeriod] = useState("");
  const [Time, setTime] = useState("");
  const [InitialInvestment, setInitialInvestment] = useState("");
  const [confidence_level, setConfidenceLevel] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onFormSubmit({ period, Time, InitialInvestment, confidence_level });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid grid-cols-2">
        <div className="input_box p-1">
          <label>Period:</label>
          <br />
          <input
            //   type="text"
            value={period}
            onChange={(event) => setPeriod(event.target.value)}
            className="rounded-lg"
            size="10"
          />
        </div>
        <div className="input_box p-1">
          <label>Time Horizon:</label>
          <br />
          <input
            //   type="text"
            value={Time}
            onChange={(event) => setTime(event.target.value)}
            className="rounded-lg"
            size="10"
          />
        </div>
      </div>

      <div className="input_box p-1">
        <label>Initial Investment :</label>
        <br />
        <input
          //   type="text"
          value={InitialInvestment}
          onChange={(event) => setInitialInvestment(event.target.value)}
          className="rounded-lg"
        />
      </div>
      <div className="input_box p-1">
        <label>Confidence Level:</label>
        <br />
        <input
          //   type="text"
          value={confidence_level}
          onChange={(event) => setConfidenceLevel(event.target.value)}
          className="rounded-lg"
        />
      </div>
      <button
        type="submit"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-1.5 mr-1 mb-1 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
      >
        Submit
      </button>
    </form>
  );
};

export default Form;
