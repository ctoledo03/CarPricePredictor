import React from 'react';

const Result = ({ price }) => {
  return (
    <div className="mt-4">
      {price === null ? (
        <div className="card border-danger">
          <div className="card-body text-danger">
            <h5 className="card-title">Prediction Failed</h5>
            <p className="card-text">Please check your inputs and try again.</p>
          </div>
        </div>
      ) : (
        <div className="card border-success">
          <div className="card-body text-success">
            <h5 className="card-title">Estimated Price</h5>
            <p className="card-text fs-4 fw-bold">${price.toLocaleString()}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Result;
