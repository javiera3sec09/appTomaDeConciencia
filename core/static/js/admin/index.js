document.addEventListener("DOMContentLoaded", function() {
  // 1. Gráfico de Evolución de Partidas (Line Chart con Curvas y Gradiente)
  const ctxLine = document.getElementById('lineChartEvolucion').getContext('2d');
  
  // Gradientes
  const gradPurple = ctxLine.createLinearGradient(0, 0, 0, 180);
  gradPurple.addColorStop(0, 'rgba(139, 92, 246, 0.45)');
  gradPurple.addColorStop(1, 'rgba(139, 92, 246, 0.0)');

  const gradCyan = ctxLine.createLinearGradient(0, 0, 0, 180);
  gradCyan.addColorStop(0, 'rgba(6, 182, 212, 0.35)');
  gradCyan.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

  new Chart(ctxLine, {
    type: 'line',
    data: {
      labels: ['1', '5', '10', '15', '20', '25', '30'],
      datasets: [
        {
          label: 'Partidas',
          data: [85, 110, 75, 145, 120, 165, 195],
          borderColor: '#8b5cf6',
          backgroundColor: gradPurple,
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 5,
        },
        {
          label: 'Victorias',
          data: [55, 78, 50, 105, 88, 122, 150],
          borderColor: '#06b6d4',
          backgroundColor: gradCyan,
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 5,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#171c38',
          titleColor: '#fff',
          bodyColor: '#cbd5e1',
          borderColor: '#2e3768',
          borderWidth: 1,
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.04)' },
          ticks: { color: '#64748b', font: { size: 10 } }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.04)' },
          ticks: { color: '#64748b', font: { size: 10 }, stepSize: 50 },
          suggestedMax: 200,
          suggestedMin: 0
        }
      }
    }
  });

  // 2. Gráfico de Resultados (Donut Chart con Centro)
  const ctxDonut = document.getElementById('donutChartResultados').getContext('2d');
  new Chart(ctxDonut, {
    type: 'doughnut',
    data: {
      labels: ['Victorias', 'Derrotas', 'Abandonadas'],
      datasets: [{
        data: [
          Number(document.getElementById('donutChartResultados')?.dataset?.victorias || 0),
          Number(document.getElementById('donutChartResultados')?.dataset?.derrotas || 0),
          Number(document.getElementById('donutChartResultados')?.dataset?.abandonadas || 0)
        ],
        backgroundColor: ['#10b981', '#8b5cf6', '#ef4444'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '76%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#171c38',
          bodyColor: '#fff',
          borderColor: '#2e3768',
          borderWidth: 1,
        }
      }
    }
  });
});
