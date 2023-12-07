import React from 'react' // nạp thư viện react
import ReactDOM from 'react-dom/client' // nạp thư viện react-dom

import { Chart } from './App.js'
function App() {
    return (
        <div>
            <h1>Biểu đồ danh mục đầu tư hiệu quả nhất</h1>
            <div>
                <Chart />
            </div>
        </div>
    )   
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
