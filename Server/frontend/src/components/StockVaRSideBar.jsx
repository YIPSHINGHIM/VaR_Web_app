import React from "react";
import { useForm } from "react-hook-form";

const StockVaRSideBar = ({ onSubmit }) => {
  const { register, handleSubmit } = useForm();

  let tempData = sessionStorage.getItem("stockKey");
  if (tempData) {
    tempData = JSON.parse(tempData);
  } else {
    console.log("Nothing in the loacl session storage");
  }

  console.log(tempData);

  return (
    <div className="bg-gray-200 p-4 h-screen">
      <h2 className="text-2xl mb-4">Stock VaR Calculator</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-3">
          <label htmlFor="stock_list" className="block mb-2">
            Stock List
          </label>
          <input
            type="text"
            id="stock_list"
            {...register("stock_list")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={
              tempData ? tempData.stock_list : "Stock list (comma separated)"
            }
          />
        </div>

        <div className="mb-3">
          <label htmlFor="portfolio_weights" className="block mb-2">
            Portfolio Weights
          </label>
          <input
            type="text"
            id="portfolio_weights"
            {...register("portfolio_weights")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={
              tempData
                ? tempData.portfolio_weights
                : "Portfolio weights (comma separated)"
            }
          />
        </div>

        <div className="mb-3">
          <label htmlFor="period" className="block mb-2">
            Period
          </label>
          <input
            type="text"
            id="period"
            {...register("period")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={tempData ? tempData.period : "Period"}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="Time" className="block mb-2">
            Time Horizon
          </label>
          <input
            type="text"
            id="Time"
            {...register("Time")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={tempData ? tempData.Time : "Time horizon"}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="InitialInvestment" className="block mb-2">
            Initial Investment
          </label>
          <input
            type="text"
            id="InitialInvestment"
            {...register("InitialInvestment")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={
              tempData ? tempData.InitialInvestment : "Initial investment"
            }
          />
        </div>

        <div className="mb-3">
          <label htmlFor="confidence_level" className="block mb-2">
            Confidence Level
          </label>
          <input
            type="text"
            id="confidence_level"
            {...register("confidence_level")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder={
              tempData ? tempData.confidence_level : "Confidence level"
            }
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 text-white p-2 rounded"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default StockVaRSideBar;
