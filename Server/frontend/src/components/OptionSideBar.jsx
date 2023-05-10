import React, { useState } from "react";

// const OptionSiderBar = () => {
//   return (
//     <div>
//       <h1 className="text-3xl">Testing </h1>

//     </div>
//   );
// };



const OptionSideBar = ({
  stockList,
  optionType,
  strikePrice,
  expirationDate,
  portfolioWeights,
  riskFreeRate,
  confidenceLevel,
  numberOfOptions,
  handleFormSubmit,
  handleFormSubmit2,
  handleFormSubmit3,
  handleFormSubmit4,
  handleFormSubmit5,
  handleFormSubmit6,
  handleFormSubmit7,
  handleFormSubmit8,
}) => {
  const [inputValues, setInputValues] = useState({
    stock_list: "",
    option_type: "",
    strike_price: "",
    expiration_date: "",
    portfolio_weights: "",
    risk_free_rate: "",
    confidence_level: "",
    number_of_options: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setInputValues({ ...inputValues, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleFormSubmit(inputValues.stock_list.split(","));
    handleFormSubmit2(inputValues.option_type.split(","));
    handleFormSubmit3(inputValues.strike_price.split(","));
    handleFormSubmit4(inputValues.expiration_date.split(","));
    handleFormSubmit5(inputValues.portfolio_weights.split(","));
    handleFormSubmit6(inputValues.risk_free_rate);
    handleFormSubmit7(inputValues.confidence_level);
    handleFormSubmit8(inputValues.number_of_options.split(","));
  };

  return (
    <div className="OptionSideBar">
      <form onSubmit={handleSubmit}>
        <div>
          <label>Stock List: </label>
          <input
            type="text"
            name="stock_list"
            value={inputValues.stock_list}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Option Type: </label>
          <input
            type="text"
            name="option_type"
            value={inputValues.option_type}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Strike Price: </label>
          <input
            type="text"
            name="strike_price"
            value={inputValues.strike_price}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Expiration Date: </label>
          <input
            type="text"
            name="expiration_date"
            value={inputValues.expiration_date}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Portfolio Weights: </label>
          <input
            type="text"
            name="portfolio_weights"
            value={inputValues.portfolio_weights}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Risk-Free Rate: </label>
          <input
            type="text"
            name="risk_free_rate"
            value={inputValues.risk_free_rate}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Confidence Level: </label>
          <input
            type="text"
            name="confidence_level"
            value={inputValues.confidence_level}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Number of Options: </label>
          <input
            type="text"
            name="number_of_options"
            value={inputValues.number_of_options}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      
    </div>
  );
};

export default OptionSideBar;
