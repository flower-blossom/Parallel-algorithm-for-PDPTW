import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const databases = require('./data.json')

// print all databases
var listName = []
var listProportion = []
databases.forEach(db => {
    listName.push(`${db.name}`)
    listProportion.push(`${db.proportion}`)
    // console.log(`${db.name}: ${db.proportion}`);
});

export const dataChart = {
  labels: listName,
  datasets: [
    {
      label: 'Số đầu tư',
      data: listProportion,
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1,
    },
  ],
};

export function Chart() {
  return <Doughnut data={dataChart} width={400} height={400} options={{ maintainAspectRatio: false }}/>;
}