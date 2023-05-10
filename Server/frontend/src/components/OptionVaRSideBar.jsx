import React from "react";
import { useForm } from "react-hook-form";

const OptionVaRSideBar = ({ onSubmit }) => {
  const { register, handleSubmit } = useForm();

  return (
    <div className="bg-gray-200 p-4 h-screen">
      <h2 className="text-2xl mb-4">Option VaR Calculator</h2>
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
            placeholder="Stock list (comma separated)"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="option_type" className="block mb-2">
            Option Type
          </label>
          <input
            type="text"
            id="option_type"
            {...register("option_type")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Option type (comma separated)"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="strike_price" className="block mb-2">
            Strike Price
          </label>
          <input
            type="text"
            id="strike_price"
            {...register("strike_price")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Strike price (comma separated)"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="expiration_date" className="block mb-2">
            Expiration Date
          </label>
          <input
            type="text"
            id="expiration_date"
            {...register("expiration_date")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="yyyy-mm-dd (comma separated) "
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
            placeholder="Portfolio weights (comma separated)"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="risk_free_rate" className="block mb-2">
            Risk-Free Rate
          </label>
          <input
            type="text"
            id="risk_free_rate"
            {...register("risk_free_rate")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Risk-free rate"
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
            placeholder="Confidence level"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="number_of_options" className="block mb-2">
            Number of Options
          </label>
          <input
            type="text"
            id="number_of_options"
            {...register("number_of_options")}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Number of options (comma separated)"
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

export default OptionVaRSideBar;
