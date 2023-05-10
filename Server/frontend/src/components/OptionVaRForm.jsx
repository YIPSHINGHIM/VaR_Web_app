import React, { useState } from "react";

const OptionVaRForm = ({ onSubmit }) => {
  const [inputs, setInputs] = useState({
    stock_list: [],
    option_type: [],
    strike_price: [],
    expiration_date: [],
    portfolio_weights: [],
    risk_free_rate: "",
    confidence_level: "",
    number_of_options: [],
  });

  const handleChange = (e, field, index) => {
    if (
      [
        "stock_list",
        "option_type",
        "strike_price",
        "expiration_date",
        "portfolio_weights",
        "number_of_options",
      ].includes(field)
    ) {
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

  const renderMultipleInputs = (field, label) =>
    inputs[field].map((_, index) => (
      <div key={`${field}-${index}`}>
        <label htmlFor={`${field}-${index}`}>
          {label} {index + 1}:
        </label>
        <input
          id={`${field}-${index}`}
          type="text"
          value={inputs[field][index]}
          onChange={(e) => handleChange(e, field, index)}
        />
      </div>
    ));

  const addInput = (field) => {
    setInputs({ ...inputs, [field]: [...inputs[field], ""] });
  };

  return (
    <form onSubmit={handleSubmit}>
      {renderMultipleInputs("stock_list", "Stock")}
      <button type="button" onClick={() => addInput("stock_list")}>
        Add Stock
      </button>

      {renderMultipleInputs("option_type", "Option Type")}
      <button type="button" onClick={() => addInput("option_type")}>
        Add Option Type
      </button>

      {renderMultipleInputs("strike_price", "Strike Price")}
      <button type="button" onClick={() => addInput("strike_price")}>
        Add Strike Price
      </button>

      {renderMultipleInputs("expiration_date", "Expiration Date")}
      <button type="button" onClick={() => addInput("expiration_date")}>
        Add Expiration Date
      </button>

      {renderMultipleInputs("portfolio_weights", "Portfolio Weight")}
      <button type="button" onClick={() => addInput("portfolio_weights")}>
        Add Portfolio Weight
      </button>

      {renderMultipleInputs("number_of_options", "Number of Options")}
      <button type="button" onClick={() => addInput("number_of_options")}>
        Add Number of Options
      </button>

      <div>
        <label htmlFor="risk_free_rate">Risk-free Rate:</label>
        <input
          id="risk_free_rate"
          type="text"
          value={inputs.risk_free_rate}
          onChange={(e) => handleChange(e, "risk_free_rate")}
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

export default OptionVaRForm;
