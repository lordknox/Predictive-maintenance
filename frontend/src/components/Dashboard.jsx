import React, { useState } from "react";
import axios from "axios";
import Chart from "./Chart";

export default function Dashboard() {
  const [rul, setRul] = useState(null);
  const [loading, setLoading] = useState(false);

  const getPrediction = async () => {
    setLoading(true);

    const sampleData = Array(30)
      .fill(0)
      .map((_, i) =>
        Array(24).fill(0).map(() => 0.5 + i * 0.01)
      );

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", {
        data: sampleData,
      });

      setRul(res.data.predicted_RUL);
    } catch (err) {
      console.error(err);
      alert("Error fetching prediction");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>Machine Health Dashboard</h2>

      <button onClick={getPrediction} disabled={loading}>
        {loading ? "Predicting..." : "Predict RUL"}
      </button>

      {rul !== null && (
        <>
          <Chart rul={rul} />

          <div style={{ marginTop: "30px" }}>
            <h3>Remaining Useful Life: {rul.toFixed(2)}</h3>

            <div
              style={{
                width: "300px",
                height: "20px",
                background: "#ddd",
                margin: "10px auto",
                borderRadius: "10px",
              }}
            >
              <div
                style={{
                  width: `${Math.min(rul, 100)}%`,
                  height: "100%",
                  background:
                    rul > 80 ? "green" : rul > 40 ? "orange" : "red",
                  borderRadius: "10px",
                }}
              ></div>
            </div>

            {rul > 80 && <p style={{ color: "green" }}>Healthy ✅</p>}
            {rul <= 80 && rul > 40 && (
              <p style={{ color: "orange" }}>Warning ⚠️</p>
            )}
            {rul <= 40 && <p style={{ color: "red" }}>Critical 🚨</p>}
          </div>
        </>
      )}
    </div>
  );
}