import React, { useState } from "react";

function Form({ onFormSubmit, title }) {
  const [inputs, setInputs] = useState([{ value: "" }]);

  const handleInputChange = (index, event) => {
    const values = [...inputs];
    values[index].value = event.target.value;
    setInputs(values);
  };

  const handleAddInput = () => {
    setInputs([...inputs, { value: "" }]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const formValues = inputs.map((input) => input.value);
    onFormSubmit(formValues);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label className="">{title} :</label>
      {inputs.map((input, index) => (
        <div className="input_box p-1">
          <input
            key={index}
            value={input.value}
            onChange={(event) => handleInputChange(index, event)}
            size="10"
            className="rounded-lg"
          />
        </div>
      ))}

      <button
        type="button"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-1.5 mr-1 mb-1 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
        onClick={handleAddInput}
      >
        Add {title}
      </button>
      <button
        type="submit"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-1.5 mr-1 mb-1 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
      >
        Submit
      </button>
    </form>
  );
}

export default Form;
