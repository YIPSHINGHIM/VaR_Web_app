import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const TimeSeriesGraph = ({ data, title }) => {
  const [elementWidth, setElementWidth] = useState(null);

  let element = null;

  const getElementWidth = () => {
    return element.offsetWidth;
  };

  useEffect(() => {
    setElementWidth(getElementWidth());
    window.addEventListener("resize", handleWindowResize);
    return () => window.removeEventListener("resize", handleWindowResize);
  }, []);

  const handleWindowResize = () => {
    setElementWidth(getElementWidth());
  };

  let plotData = [];

  if (data) {
    Object.entries(data).map(([ticker, ticker_value]) => {
      const Date = Object.keys(ticker_value);
      const ClosingPrice = Object.values(ticker_value);

      plotData.push({
        x: Date,
        y: ClosingPrice,
        type: "scatter",
        name: ticker,
        mode: "lines",
      });
    });
  }

  const range = ["2023-02-28", "2023-02-28"];

  return (
    <div className="TimeSeriesGraph" ref={(el) => (element = el)}>
      <Plot
        data={plotData}
        layout={{
          title: title,
          xaxis: {
            autorange: true,
            range: range,
            rangeselector: {
              buttons: [
                {
                  count: 1,
                  label: "1m",
                  step: "month",
                  stepmode: "backward",
                },
                {
                  count: 6,
                  label: "6m",
                  step: "month",
                  stepmode: "backward",
                },
                { step: "all" },
              ],
            },
            rangeslider: { range: range },
            type: "date",
          },
          yaxis: {
            autorange: true,
            range: [86.8700008333, 138.870004167],
            type: "linear",
          },
          width: elementWidth,
        }}
      />
    </div>
  );
};

export default TimeSeriesGraph;
