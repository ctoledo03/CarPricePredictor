import React, { useState } from 'react';
import CarForm from './CarForm';
import Result from './Result';

function App() {
  const [predictedPrice, setPredictedPrice] = useState(null);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Used Car Price Predictor</h1>
      <CarForm onPrediction={setPredictedPrice} />
      {predictedPrice !== null && <Result price={predictedPrice} />}
    </div>
  );
}

export default App;
