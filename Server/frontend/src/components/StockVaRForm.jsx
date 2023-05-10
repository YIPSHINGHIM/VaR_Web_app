import React, { useState } from "react";

const StockVaRForm = ({ onSubmit }) => {
  const [inputs, setInputs] = useState({
    stock_list: [],
    portfolio_weights: [],
    period: "",
    time: "",
    initialInvestment: "",
    confidence_level: "",
  });

  const handleChange = (e, field, index) => {
    if (['stock_list', 'portfolio_weights'].includes(field)) {
      const newInputs = { ...inputs };
      newInputs[field][index] = e.target.value;
      setInputs(newInputs);
    } else {
      setInputs({ ...inputs, [field]: e.target.value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(inputs);
  };

  const renderMultipleInputs = (field, label) => (
    inputs[field].map((_, index) => (
      <div key={`${field}-${index}`}>
        <label htmlFor={`${field}-${index}`}>{label} {index + 1}:</label>
        <input
          id={`${field}-${index}`}
          type="text"
          value={inputs[field][index]}
          onChange={(e) => handleChange(e, field, index)}
        />
      </div>
    ))
  );

  const addInput = (field) => {
    setInputs({ ...inputs, [field]: [...inputs[field], ""] });
  };

  return (
    <form onSubmit={handleSubmit}>
      {renderMultipleInputs("stock_list", "Stock")}
      <button type="button" onClick={() => addInput("stock_list")}>
        Add Stock
      </button>

      {renderMultipleInputs("portfolio_weights", "Portfolio Weight")}
      <button type="button" onClick={() => addInput("portfolio_weights")}>
        Add Portfolio Weight
      </button>

      <div>
        <label htmlFor="period">Period:</label>
        <input
          id="period"
          type="text"
          value={inputs.period}
          onChange={(e) => handleChange(e, "period")}
        />
      </div>

      <div>
        <label htmlFor="time">Time Horizon:</label>
        <input
          id="time"
          type="text"
          value={inputs.time}
          onChange={(e) => handleChange(e, "time")}
        />
      </div>

      <div>
        <label htmlFor="initialInvestment">Initial Investment:</label>
        <input
          id="initialInvestment"
          type="text"
          value={inputs.initialInvestment}
          onChange={(e) => handleChange(e, "initialInvestment")}
        />
      </div>

      <div>
        <label htmlFor="confidence_level">Confidence Level:</label>
        <input
          id="confidence_level"
          type="text"
          value={inputs.confidence_level}
          onChange={(e) => handleChange(e, "confidence_level")}
        />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
};

export default StockVaRForm;
