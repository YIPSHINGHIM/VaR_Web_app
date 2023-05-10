import React from "react";
import Form from "./Form";
import FormForOther from "./FormForOther";

const SideBar = ({
  ticket,
  weight,
  Input,
  handleFormSubmit,
  handleFormSubmit2,
  handleFormSubmit3,
  handleButtonClick,
  data,
}) => {
  return (
    <div className="left col-span-2 bg-teal-500 min-h-screen h-fit row-span-full">
      <h3>
        IMPORTANT: You need to type the Stock Ticket to see view the chart
      </h3>

      <FormForOther onFormSubmit={handleFormSubmit3} />

      <div className="grid grid-cols-2">
        <div className="StockForm px-1">
          <Form onFormSubmit={handleFormSubmit} title="Stock" />
        </div>
        <div className="WeightForm px-1">
          <Form onFormSubmit={handleFormSubmit2} title="Weight" />
        </div>
      </div>

      {Object.entries(Input).map(([key, value]) => (
        <p className="text-xl" key={key}>
          {key}: {value}
        </p>
      ))}
      {ticket.map((value, index) => (
        <p className="text-xl" key={index}>
          {value}
        </p>
      ))}
      {weight.map((value, index) => (
        <p className="text-xl" key={index}>
          {value}
        </p>
      ))}

      <div className="fetchDataButton">
        <button
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-1.5 mr-1 mb-1 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          onClick={handleButtonClick}
        >
          Fetch Data
        </button>
        {data ? (
          <p>{JSON.stringify(data, null, 2)}</p>
        ) : (
          <p>Waiting for input</p>
        )}
      </div>
    </div>
  );
};

export default SideBar;
