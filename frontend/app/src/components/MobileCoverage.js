import React, { useState } from 'react';

function App() {
  // State for the address and the result
  const [address, setAddress] = useState('');
  const [result, setResult] = useState('');

  // Function to simulate the query
  const queryAddress = () => {
    if (!address) {
      setResult('Please enter an address.');
      return;
    }

    setResult(`Query result: ${address}`);
  };

return (
    <div className="App">
        <h1>Mobile Network Coverage</h1>
        <div className="form-container">
            <input
                type="text"
                placeholder="Enter an address"
                value={address}
                style={{ width: '600px', height: '30px', marginRight: '10px' }}
                onChange={(e) => setAddress(e.target.value)}
            />
            <button
                style={{ height: '30px' }}
                onClick={queryAddress}>Search
            </button>
        </div>
        <p>{result}</p>
    </div>
);
}

export default App;
