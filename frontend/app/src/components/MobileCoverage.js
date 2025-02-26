import getMobileCoverage from "../services/api";
import React, { useState } from 'react';

function App() {
  // State for the address and the result
  const [address, setAddress] = useState('');
  const [result, setResult] = useState('');

const handleSearch = async () => {
    try {
        const data = await getMobileCoverage(address);
        setResult(data);
    } catch (error) {
        setResult('Error fetching data');
    }
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
                onClick={handleSearch}> Search
            </button>
        </div>
        { result && (<div>
            <h2>Result:</h2>
                <pre>{typeof result === 'object' ? JSON.stringify(result, null, 2) : result}</pre>
        </div> )}
    </div>
);
}

export default App;
