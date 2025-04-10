import React, { useState } from 'react';
import axios from 'axios';
import {
  BRANDS,
  FUEL_TYPES,
  TRANSMISSIONS,
  EXTERIOR_COLORS,
  INTERIOR_COLORS
} from './constants/dropdownOptions';
 
const CarForm = ({ onPrediction }) => {
  const [formData, setFormData] = useState({
    model_year: '',
    milage: '',
    brand: '',
    model: '',
    engine: '',
    fuel_type: '',
    transmission: '',
    ext_col: '',
    int_col: '',
    clean_title: '',
    accident: ''
  });
 
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', formData);
      onPrediction(response.data.predicted_price);
    } catch (error) {
      console.error('Prediction request failed:', error);
      onPrediction(null);
    }
  };
 
  return (
    <div className="card shadow p-4 mb-4">
      <h3 className="mb-3">Used Car Details</h3>
      <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="col-md-6 mb-3">
            <label>Model Year</label>
            <input type="number" name="model_year" className="form-control" required onChange={handleChange} />
          </div>
          <div className="col-md-6 mb-3">
            <label>Mileage (mi)</label>
            <input type="number" name="milage" className="form-control" required onChange={handleChange} />
          </div>
          <div className="col-md-6 mb-3">
            <label>Brand</label>
            <select name="brand" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              {BRANDS.map((brand) => (
                <option key={brand} value={brand}>{brand}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6 mb-3">
            <label>Model (optional)</label>
            <input type="text" name="model" className="form-control" onChange={handleChange} />
          </div>
          <div className="col-md-6 mb-3">
            <label>Engine (optional)</label>
            <input type="text" name="engine" className="form-control" onChange={handleChange} />
          </div>
          <div className="col-md-6 mb-3">
            <label>Fuel Type</label>
            <select name="fuel_type" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              {FUEL_TYPES.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6 mb-3">
            <label>Transmission</label>
            <select name="transmission" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              {TRANSMISSIONS.map((tran) => (
                <option key={tran} value={tran}>{tran}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6 mb-3">
            <label>Exterior Color</label>
            <select name="ext_col" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              {EXTERIOR_COLORS.map((color) => (
                <option key={color} value={color}>{color}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6 mb-3">
            <label>Interior Color</label>
            <select name="int_col" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              {INTERIOR_COLORS.map((color) => (
                <option key={color} value={color}>{color}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6 mb-3">
            <label>Clean Title</label>
            <select name="clean_title" className="form-control" required onChange={handleChange}>
              <option value="">Select</option>
              <option value="1">Yes</option>
              <option value="0">No</option>
            </select>
          </div>
          <div className="col-md-12 mb-3">
            <label>Accident History</label>
            <input type="text" name="accident" className="form-control" required onChange={handleChange} />
          </div>
        </div>
        <button type="submit" className="btn btn-primary mt-3">Predict Price</button>
      </form>
    </div>
  );
};
 
export default CarForm;